"""
Real-time audio capture and speech-to-text transcription.

Captures system audio (the interview call) and transcribes it in real-time
using OpenAI's Whisper model running locally via faster-whisper.
"""

import asyncio
import queue
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


class AudioTranscriber:
    """Captures audio from a selected input device and transcribes in real-time."""

    def __init__(
        self,
        model_size: str = "base.en",
        device_index: int | None = None,
        sample_rate: int = 16000,
        chunk_duration: float = 3.0,
        silence_threshold: float = 0.01,
    ):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.silence_threshold = silence_threshold
        self.device_index = device_index
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self._running = False
        self._stream = None

        print(f"[transcriber] Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )
        print("[transcriber] Model loaded.")

    @staticmethod
    def list_devices() -> list[dict]:
        """Return available audio input devices."""
        devices = sd.query_devices()
        inputs = []
        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                inputs.append({"index": i, "name": d["name"], "channels": d["max_input_channels"]})
        return inputs

    def _audio_callback(self, indata: np.ndarray, frames: int, time_info, status):
        """Called by sounddevice for each audio chunk."""
        if status:
            print(f"[audio] {status}")
        self.audio_queue.put(indata.copy())

    def start_stream(self):
        """Start capturing audio from the selected device."""
        self._running = True
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=int(self.sample_rate * self.chunk_duration),
            device=self.device_index,
            channels=1,
            dtype="float32",
            callback=self._audio_callback,
        )
        self._stream.start()
        print(f"[audio] Capturing from device: {self.device_index or 'default'}")

    def stop_stream(self):
        """Stop the audio capture stream."""
        self._running = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        print("[audio] Stream stopped.")

    def _is_silence(self, audio: np.ndarray) -> bool:
        """Check if an audio chunk is silence."""
        rms = np.sqrt(np.mean(audio**2))
        return rms < self.silence_threshold

    async def transcribe_stream(self, on_transcript: callable):
        """
        Continuously pull audio from the queue, transcribe, and call the callback.

        Args:
            on_transcript: async callable(speaker: str, text: str) invoked
                           each time a new segment is transcribed.
        """
        buffer = np.array([], dtype="float32")
        min_buffer = self.sample_rate * 2  # at least 2 seconds before transcribing

        while self._running:
            try:
                chunk = self.audio_queue.get(timeout=0.5)
            except queue.Empty:
                await asyncio.sleep(0.05)
                continue

            audio = chunk.flatten()

            if self._is_silence(audio):
                # If we have buffered speech followed by silence, flush the buffer
                if len(buffer) >= min_buffer:
                    await self._transcribe_buffer(buffer, on_transcript)
                    buffer = np.array([], dtype="float32")
                continue

            buffer = np.concatenate([buffer, audio])

            # Transcribe when buffer is long enough
            if len(buffer) >= self.sample_rate * self.chunk_duration * 2:
                await self._transcribe_buffer(buffer, on_transcript)
                buffer = np.array([], dtype="float32")

        # Flush remaining buffer
        if len(buffer) >= min_buffer:
            await self._transcribe_buffer(buffer, on_transcript)

    async def _transcribe_buffer(self, audio: np.ndarray, on_transcript: callable):
        """Run Whisper on a buffer and invoke the callback with results."""
        loop = asyncio.get_event_loop()
        segments, info = await loop.run_in_executor(
            None,
            lambda: self.model.transcribe(
                audio,
                beam_size=3,
                language="en",
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            ),
        )

        for segment in segments:
            text = segment.text.strip()
            if text and len(text) > 3:
                await on_transcript("Interviewer", text)

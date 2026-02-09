"""
FastAPI server that ties together audio capture, transcription, and AI response generation.

Serves a WebSocket endpoint for the real-time dashboard UI and coordinates
the audio pipeline with the response engine.
"""

import asyncio
import json
import time
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from audio_capture import AudioTranscriber
from response_engine import ResponseEngine

app = FastAPI(title="Interview Response Assistant")

# Serve static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Global state
transcriber: AudioTranscriber | None = None
response_engine = ResponseEngine()
active_connections: list[WebSocket] = []


@app.get("/")
async def root():
    """Serve the dashboard UI."""
    return FileResponse(str(static_dir / "index.html"))


async def broadcast(message: dict):
    """Send a message to all connected WebSocket clients."""
    dead = []
    for ws in active_connections:
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        active_connections.remove(ws)


async def on_transcript(speaker: str, text: str):
    """Called when new transcription is available."""
    timestamp = time.time()

    # Broadcast the transcript to all clients
    await broadcast({
        "type": "transcript",
        "speaker": speaker,
        "text": text,
        "timestamp": timestamp,
    })

    # Generate AI response
    await broadcast({"type": "response_start", "question": text})

    try:
        async for chunk in response_engine.generate_response_stream(text):
            await broadcast({"type": "response_chunk", "text": chunk})
    except Exception as e:
        await broadcast({"type": "error", "message": f"Response generation failed: {e}"})

    await broadcast({"type": "response_done"})


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """Main WebSocket endpoint for the dashboard."""
    global transcriber

    await ws.accept()
    active_connections.append(ws)

    transcribe_task = None

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            msg_type = msg.get("type")

            if msg_type == "list_devices":
                devices = AudioTranscriber.list_devices()
                await ws.send_json({"type": "devices", "devices": devices})

            elif msg_type == "start":
                device_index = msg.get("device_index")
                if transcriber:
                    transcriber.stop_stream()

                transcriber = AudioTranscriber(
                    model_size="base.en",
                    device_index=device_index,
                )
                transcriber.start_stream()

                await ws.send_json({"type": "mic_status", "active": True})

                # Start transcription loop in the background
                transcribe_task = asyncio.create_task(
                    transcriber.transcribe_stream(on_transcript)
                )

            elif msg_type == "stop":
                if transcriber:
                    transcriber.stop_stream()
                    transcriber = None
                if transcribe_task:
                    transcribe_task.cancel()
                    transcribe_task = None
                await ws.send_json({"type": "mic_status", "active": False})

            elif msg_type == "manual_input":
                # Manual mode: user types the interviewer's question
                text = msg.get("text", "").strip()
                if text:
                    await on_transcript("Interviewer", text)

            elif msg_type == "clear_history":
                response_engine.conversation_history.clear()

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[ws] Error: {e}")
    finally:
        if ws in active_connections:
            active_connections.remove(ws)
        if transcriber:
            transcriber.stop_stream()
        if transcribe_task:
            transcribe_task.cancel()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)

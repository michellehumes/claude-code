# Interview Response Assistant

Real-time interview coaching system that listens to your phone call, transcribes the interviewer's questions, and immediately generates suggested responses based on your experience profile.

## How It Works

```
Phone Call Audio --> Microphone/System Audio Capture
                        |
                        v
                  Whisper (Speech-to-Text)
                        |
                        v
                  Claude AI (Response Generation)
                        |
                        v
                  Web Dashboard (Live Display)
```

1. **Audio Capture**: Captures audio from your microphone or system audio (via virtual audio cable)
2. **Transcription**: Uses faster-whisper (local, offline) to transcribe speech in real-time
3. **AI Coach**: Sends transcribed questions to Claude, which generates tailored responses using your experience profile
4. **Live Dashboard**: Displays the transcript and suggested responses in a split-panel web UI via WebSocket streaming

## Setup

### 1. Install Dependencies

```bash
cd interview-response-assistant
pip install -r requirements.txt
```

### 2. Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. Customize Your Experience Profile

Edit `experience.json` with your actual:
- Work experience and highlights
- Skills (technical + soft)
- Education
- Key achievements
- Pre-written answers to common questions (tell me about yourself, why are you leaving, etc.)

The more detail you add, the better the AI responses will be.

### 4. Audio Setup

**Option A: Microphone (simplest)**
Place your phone on speaker and let your computer microphone pick up the audio.

**Option B: Virtual Audio Cable (best quality)**
Route your phone call audio directly into the system:

- **Mac**: Install [BlackHole](https://existential.audio/blackhole/) - creates a virtual audio device
- **Windows**: Install [VB-Cable](https://vb-audio.com/Cable/) - creates a virtual audio device
- **Linux**: Use PulseAudio's built-in monitor devices

Then select the virtual device in the dashboard dropdown.

### 5. Run

```bash
python server.py
```

Open your browser to **http://localhost:8765**

## Usage

### Live Mode (Automatic)
1. Select your audio input device from the dropdown
2. Click **Start Listening**
3. The system transcribes in real-time and generates responses as the interviewer speaks
4. Read the suggested responses from the right panel

### Manual Mode (Fallback)
If audio capture doesn't work well in your environment:
1. Switch to **Manual** mode in the header
2. Type or paste the interviewer's question in the input field at the bottom
3. Press Enter - the AI will generate a response immediately

This is also useful for practicing before an interview.

## Project Structure

```
interview-response-assistant/
├── server.py              # FastAPI + WebSocket server (main entry point)
├── audio_capture.py       # Audio device capture + Whisper transcription
├── response_engine.py     # Claude AI response generation with streaming
├── experience.json        # Your experience profile (customize this!)
├── requirements.txt       # Python dependencies
├── static/
│   └── index.html         # Live dashboard UI
└── README.md
```

## Tips for Best Results

- **Fill out experience.json thoroughly** - include specific numbers, metrics, and examples
- **Add common_answers** for questions you know will come up (tell me about yourself, why this company, etc.)
- **Use a virtual audio cable** for clean audio without background noise
- **Position the dashboard** on a second monitor or to the side of your video call window
- **Don't read verbatim** - use the key points as talking points and speak naturally
- **Practice first** using manual mode to see what kinds of responses the system generates

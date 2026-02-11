#!/bin/bash
# Interview Response Assistant — One-click setup for Mac
# Run this with: bash setup.sh

set -e

echo ""
echo "==================================="
echo " Interview Response Assistant Setup"
echo "==================================="
echo ""

# Step 1: Clone the repo if needed
if [ ! -d "$HOME/claude-code" ]; then
    echo "[1/4] Cloning repository..."
    git clone https://github.com/michellehumes/claude-code.git "$HOME/claude-code"
else
    echo "[1/4] Repository already exists, pulling latest..."
    cd "$HOME/claude-code"
    git fetch origin claude/interview-response-assistant-Cstiq
    git checkout claude/interview-response-assistant-Cstiq
    git pull origin claude/interview-response-assistant-Cstiq
fi

cd "$HOME/claude-code/interview-response-assistant"

# Step 2: Create virtual environment
echo "[2/4] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Install dependencies
echo "[3/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Check for API key
echo ""
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your-key" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-your-actual-key-here" ]; then
    echo "============================================"
    echo " IMPORTANT: Set your Anthropic API key!"
    echo "============================================"
    echo ""
    echo " Run this before starting the server:"
    echo ""
    echo "   export ANTHROPIC_API_KEY=\"sk-ant-xxxxx\""
    echo ""
    echo " Get your key at: https://console.anthropic.com/settings/keys"
    echo ""
fi

echo "[4/4] Setup complete!"
echo ""
echo "==================================="
echo " TO START THE SERVER:"
echo "==================================="
echo ""
echo "  cd ~/claude-code/interview-response-assistant"
echo "  source venv/bin/activate"
echo "  export ANTHROPIC_API_KEY=\"your-key-here\""
echo "  python3 server.py"
echo ""
echo "  Then open: http://localhost:8765"
echo ""
echo "==================================="

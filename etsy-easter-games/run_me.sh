#!/bin/bash
# ============================================
# EASTER ETSY LISTING — One-Click Setup & Run
# ============================================
# Just run this one command in Terminal:
#   bash run_me.sh
# ============================================

echo ""
echo "============================================"
echo "  EASTER ETSY LISTING AUTOMATION"
echo "  Setting everything up for you..."
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Install it from https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Python 3 found ($(python3 --version))"

# Check for Chrome
if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✓ Google Chrome found"
else
    echo "ERROR: Google Chrome is not installed."
    echo "Download it from https://www.google.com/chrome/"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Creating virtual environment (one-time setup)..."
    python3 -m venv "$VENV_DIR" || {
        echo "ERROR: Could not create virtual environment."
        exit 1
    }
fi
echo "✓ Virtual environment ready"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install Playwright if not already installed
if ! python -c "import playwright" 2>/dev/null; then
    echo ""
    echo "Installing Playwright (one-time setup)..."
    pip install playwright --quiet || {
        echo "ERROR: Could not install Playwright."
        exit 1
    }
fi
echo "✓ Playwright installed"

# Run the automation (uses your installed Chrome, no Chromium download needed)
echo ""
echo "============================================"
echo "  LAUNCHING ETSY LISTING AUTOMATION"
echo "  Chrome will open. If you need to log in,"
echo "  do it in the browser — the script waits."
echo "============================================"
echo ""

cd "$SCRIPT_DIR/listing"
python automate_etsy_chrome.py

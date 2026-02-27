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

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || {
        echo "ERROR: Could not create virtual environment."
        exit 1
    }
fi
echo "✓ Virtual environment ready"

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"

# Install Playwright
echo ""
echo "Installing Playwright (browser automation)..."
pip install playwright --quiet || {
    echo "ERROR: Could not install Playwright."
    exit 1
}
echo "✓ Playwright installed"

# Install Chromium browser
echo ""
echo "Downloading Chromium browser (this may take a minute)..."
python -m playwright install chromium || {
    echo "ERROR: Could not install Chromium."
    exit 1
}
echo "✓ Chromium ready"

# Run the automation
echo ""
echo "============================================"
echo "  LAUNCHING ETSY LISTING AUTOMATION"
echo "  A browser window will open."
echo "  If Etsy asks for CAPTCHA/2FA, just"
echo "  complete it in the browser window."
echo "============================================"
echo ""

cd "$SCRIPT_DIR/listing"
python automate_etsy_chrome.py

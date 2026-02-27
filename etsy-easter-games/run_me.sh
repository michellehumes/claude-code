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

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Install it from https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Python 3 found"

# Install pip if needed
if ! python3 -m pip --version &> /dev/null; then
    echo "Installing pip..."
    python3 -m ensurepip --upgrade 2>/dev/null || {
        echo "ERROR: Could not install pip. Try running:"
        echo "  python3 -m ensurepip --upgrade"
        exit 1
    }
fi
echo "✓ pip found"

# Install Playwright
echo ""
echo "Installing Playwright (browser automation)..."
python3 -m pip install --user playwright --quiet
echo "✓ Playwright installed"

# Install Chromium browser
echo ""
echo "Downloading Chromium browser (this may take a minute)..."
python3 -m playwright install chromium
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

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/listing"
python3 automate_etsy_chrome.py

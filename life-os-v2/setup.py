#!/usr/bin/env python3
"""
Life OS v2 Setup Script

Run this to check dependencies and set up the project.
"""

import subprocess
import sys
import os


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def check_credentials():
    """Check for Google API credentials"""
    creds_path = "config/credentials.json"
    if os.path.exists(creds_path):
        print(f"✓ Credentials file found: {creds_path}")
        return True
    else:
        print(f"⚠ Credentials file not found: {creds_path}")
        print("  See README.md for Google API setup instructions")
        print("  (Not required for offline/export mode)")
        return False


def create_directories():
    """Create necessary directories"""
    dirs = [
        "data",
        "data/sample",
        "data/oura",
        "data/export",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"✓ Created directories: {', '.join(dirs)}")
    return True


def main():
    print("=" * 50)
    print("  Life OS v2 Setup")
    print("=" * 50)
    print()

    success = True

    if not check_python_version():
        success = False

    if not create_directories():
        success = False

    if not install_dependencies():
        success = False

    check_credentials()  # Warning only, not required

    print()
    if success:
        print("=" * 50)
        print("  Setup Complete!")
        print("=" * 50)
        print()
        print("Quick Start Options:")
        print()
        print("1. Export to Excel (no Google API needed):")
        print("   python src/main.py --export-excel --sample-data")
        print()
        print("2. Create Google Sheet (requires credentials.json):")
        print("   python src/main.py --create 'Life OS v2'")
        print()
        print("3. Import your data:")
        print("   python src/main.py --create 'Life OS v2' \\")
        print("       --transactions data/transactions.csv \\")
        print("       --oura-dir data/oura")
    else:
        print("Setup encountered errors. Please fix and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

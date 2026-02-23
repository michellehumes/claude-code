# Domino Dreams iOS Bot

Automated bot that plays Domino Dreams on your iPhone. Connects via USB, reads the screen with computer vision, and plays through chapters automatically.

## Requirements

- **macOS** computer (required for iOS USB communication)
- **Python 3.10+**
- **iPhone** with Domino Dreams installed
- **USB cable** connecting iPhone to Mac
- **Developer Mode** enabled on iPhone (Settings > Privacy & Security > Developer Mode)

## Quick Start

### 1. Install Dependencies

```bash
cd domino-dreams-bot
pip install -r requirements.txt
```

### 2. Prepare Your iPhone

1. Connect your iPhone to your Mac via USB cable
2. Unlock your iPhone and tap **Trust** if prompted
3. Enable Developer Mode:
   - Go to **Settings > Privacy & Security > Developer Mode**
   - Toggle it on and restart when prompted
4. Open **Domino Dreams** on your iPhone

### 3. Run Calibration (First Time)

This takes a screenshot and shows you what the bot detects:

```bash
python bot.py --calibrate
```

Review the output. If detection seems off, adjust thresholds in `config.yaml`.

### 4. Run the Bot

```bash
# Normal mode - plays the game
python bot.py

# Dry run - analyzes the screen without tapping
python bot.py --dry-run

# Verbose output for debugging
python bot.py --verbose
```

Press **Ctrl+C** to stop the bot at any time.

## How It Works

```
Screenshot (USB) --> OpenCV Analysis --> Decision Engine --> Touch Events (USB)
     |                    |                    |                    |
  iPhone            Detect screen        Pick action          Tap/Swipe
  screen            type, dominoes,      based on game        on iPhone
  capture           buttons, popups      strategy
```

1. **Screen Capture**: Takes screenshots from your iPhone over USB using `pymobiledevice3`
2. **Vision Analysis**: OpenCV detects which screen you're on (gameplay, menus, popups) and identifies dominoes, buttons, and interactive elements
3. **Decision Engine**: Based on the detected state, decides what to tap - prioritizes highlighted dominoes, handles popups, collects rewards, navigates menus
4. **Touch Input**: Sends tap/swipe events back to the iPhone over USB

## Game Strategy

The bot uses this priority system during gameplay:

1. **Highlighted dominoes** - The game hints at which piece to tap next
2. **Glowing/pulsing elements** - Interactive tap targets
3. **Strategic domino selection** - Prefers edge pieces and clusters (longer chains)
4. **Higher-value dominoes** - More points per tap

Between levels, the bot automatically:
- Collects rewards
- Dismisses popups
- Navigates to the next level
- Handles chapter transitions and building scenes
- Retries failed levels (configurable max retries)

## Configuration

Edit `config.yaml` to tune the bot:

| Setting | What It Does |
|---------|-------------|
| `device.screen_width/height` | Your iPhone's screen size in points |
| `device.scale_factor` | Retina scale (2 or 3) |
| `detection.match_threshold` | How confident the vision system needs to be (0.0-1.0) |
| `timing.tap_delay` | Pause between taps (seconds) |
| `timing.poll_interval` | How often to check the screen |
| `bot.max_level_retries` | Give up on a level after N fails |
| `bot.save_screenshots` | Save screenshots for debugging |

### Common iPhone Screen Sizes (points)

| Model | Width | Height |
|-------|-------|--------|
| iPhone 15 Pro Max | 430 | 932 |
| iPhone 15 Pro | 393 | 852 |
| iPhone 15 / 14 | 390 | 844 |
| iPhone SE (3rd gen) | 375 | 667 |
| iPhone 13 mini | 375 | 812 |

## Troubleshooting

### "No iOS devices found"
- Make sure your iPhone is **unlocked**
- Tap **Trust** on the "Trust This Computer?" popup
- Try a different USB cable or port
- Run `pymobiledevice3 usbmux list` to verify detection

### "Screenshot failed"
- Enable **Developer Mode** on your iPhone
- Try: `pymobiledevice3 developer dvt screenshot test.png`
- You may need to mount the developer disk image:
  ```bash
  pymobiledevice3 mounter auto-mount
  ```

### Bot can't detect game elements
1. Run `python bot.py --calibrate` and check the screenshot
2. Adjust color ranges in `config.yaml` under the `colors:` section
3. Adjust `detection.match_threshold` (lower = more sensitive)

### Bot is too fast / too slow
- Increase `timing.tap_delay` if taps are registering before animations finish
- Decrease `timing.poll_interval` for faster response

### Out of lives
The bot will wait when it detects you're out of lives. Lives refill over time, or you can manually add them in-game.

## File Structure

```
domino-dreams-bot/
├── bot.py           # Main entry point and game loop
├── ios_device.py    # iPhone connection, screenshots, touch events
├── game_vision.py   # OpenCV game state detection
├── game_logic.py    # Decision engine and game strategy
├── config.yaml      # All configurable settings
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Limitations

- Requires a Mac (pymobiledevice3 USB communication)
- Game updates may change UI elements, requiring config adjustments
- Cannot bypass in-app purchases or time-gates
- Puzzle-solving is heuristic-based, not guaranteed optimal
- Some complex levels may require manual intervention

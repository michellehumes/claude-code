#!/usr/bin/env python3
"""
Domino Dreams iOS Bot
Main entry point - connects to iPhone, runs the game-playing loop.

Usage:
    python bot.py                  # Run with default config
    python bot.py --config my.yaml # Run with custom config
    python bot.py --calibrate      # Run calibration mode
    python bot.py --dry-run        # Analyze screen without sending taps
"""

import argparse
import logging
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import yaml
import numpy as np

from ios_device import iOSDevice
from game_vision import GameVision, GameScreen, GameState
from game_logic import GameLogic, Action, BotAction

# ----------------------------------------------------------------
# Logging setup
# ----------------------------------------------------------------

def setup_logging(verbose: bool = False):
    """Configure colored logging."""
    try:
        from colorama import init, Fore, Style
        init()
        colors = {
            "DEBUG": Fore.CYAN,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
        }
    except ImportError:
        colors = {}
        Fore = type("", (), {"RESET": ""})()
        Style = type("", (), {"RESET_ALL": ""})()

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            color = colors.get(record.levelname, "")
            reset = Style.RESET_ALL if color else ""
            record.levelname = f"{color}{record.levelname}{reset}"
            return super().format(record)

    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    ))

    root = logging.getLogger("domino_bot")
    root.addHandler(handler)
    root.setLevel(logging.DEBUG if verbose else logging.INFO)


# ----------------------------------------------------------------
# Calibration mode
# ----------------------------------------------------------------

def run_calibration(device: iOSDevice, config: dict):
    """
    Interactive calibration mode.
    Takes a screenshot and helps the user identify game regions.
    """
    logger = logging.getLogger("domino_bot.calibrate")
    logger.info("=== CALIBRATION MODE ===")
    logger.info("Open Domino Dreams on your iPhone and navigate to a level.")
    input("Press Enter when ready...")

    frame = device.screenshot()
    if frame is None:
        logger.error("Could not capture screenshot. Check device connection.")
        return

    # Save the screenshot
    os.makedirs("calibration", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"calibration/calibration_{timestamp}.png"
    device.save_screenshot(path, frame)
    logger.info(f"Screenshot saved to {path}")

    # Run vision analysis
    vision = GameVision(config)
    state = vision.analyze(frame)

    logger.info(f"Detected screen: {state.screen.name}")
    logger.info(f"Dominoes found: {len(state.dominoes)}")
    logger.info(f"Tap targets: {len(state.tap_targets)}")

    if state.play_button:
        c = state.play_button.center
        logger.info(f"Play button at: ({c.x}, {c.y})")
    if state.close_button:
        c = state.close_button.center
        logger.info(f"Close button at: ({c.x}, {c.y})")

    for i, d in enumerate(state.dominoes):
        c = d.bbox.center
        logger.info(
            f"  Domino {i}: [{d.top_value}|{d.bottom_value}] "
            f"at ({c.x}, {c.y}) "
            f"{'[HIGHLIGHTED]' if d.is_highlighted else ''}"
        )

    logger.info("\nCalibration complete. Review the screenshot and adjust")
    logger.info("config.yaml color ranges/thresholds if detection is off.")


# ----------------------------------------------------------------
# Main bot loop
# ----------------------------------------------------------------

class DominoDreamsBot:
    """Main bot controller that orchestrates the game-playing loop."""

    def __init__(self, config: dict, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.logger = logging.getLogger("domino_bot.main")

        self.device = iOSDevice(config)
        self.vision = GameVision(config)
        self.logic = GameLogic(config)

        self.running = False
        self.start_time = None
        self.frame_count = 0
        self.screenshot_dir = Path(config["bot"]["screenshot_dir"])

        if config["bot"]["save_screenshots"]:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def start(self):
        """Connect to device and start the bot loop."""
        self.logger.info("=" * 50)
        self.logger.info("  DOMINO DREAMS BOT")
        self.logger.info("=" * 50)

        if self.dry_run:
            self.logger.info("DRY RUN MODE - No taps will be sent")

        # Connect to iPhone
        if not self.device.connect():
            self.logger.error("Failed to connect to iPhone. Exiting.")
            sys.exit(1)

        self.logger.info("Connected! Starting bot loop...")
        self.logger.info("Press Ctrl+C to stop.\n")

        self.running = True
        self.start_time = datetime.now()

        # Register signal handler for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)

        try:
            self._run_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown()

    def _run_loop(self):
        """Main bot loop: screenshot -> analyze -> decide -> act."""
        poll_interval = self.config["timing"]["poll_interval"]
        level_wait = self.config["timing"]["level_complete_wait"]
        chapter_wait = self.config["timing"]["chapter_transition_wait"]

        last_screen = GameScreen.UNKNOWN
        out_of_lives_time = None

        while self.running:
            loop_start = time.time()
            self.frame_count += 1

            # 1. Capture screenshot
            frame = self.device.screenshot()
            if frame is None:
                self.logger.warning("Screenshot failed, retrying...")
                time.sleep(2)
                continue

            # 2. Analyze game state
            state = self.vision.analyze(frame)

            # 3. Log screen transitions
            if state.screen != last_screen:
                self.logger.info(f"Screen: {state.screen.name}")
                last_screen = state.screen

                # Save screenshot on screen transitions
                if self.config["bot"]["save_screenshots"]:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = self.screenshot_dir / f"{ts}_{state.screen.name}.png"
                    self.device.save_screenshot(str(path), frame)

            # 4. Handle out-of-lives waiting
            if state.screen == GameScreen.OUT_OF_LIVES:
                if out_of_lives_time is None:
                    out_of_lives_time = datetime.now()
                    self.logger.info(
                        "Out of lives. Bot will wait for lives to refill. "
                        "You can also manually add lives."
                    )

                # After dismissing the popup, wait for lives to refill
                elapsed = (datetime.now() - out_of_lives_time).total_seconds()
                if elapsed > 30:
                    # Try to continue - lives may have refilled
                    out_of_lives_time = None

            if state.screen != GameScreen.OUT_OF_LIVES:
                out_of_lives_time = None

            # 5. Decide action
            action = self.logic.decide(state)

            # 6. Execute action
            if not self.dry_run:
                self._execute_action(action)
            else:
                if action.action != Action.WAIT and action.action != Action.NONE:
                    self.logger.info(f"[DRY RUN] Would: {action.description}")

            # 7. Extra wait for transitions
            if state.screen == GameScreen.LEVEL_COMPLETE:
                time.sleep(level_wait)
            elif state.screen == GameScreen.CHAPTER_COMPLETE:
                time.sleep(chapter_wait)

            # 8. Status update every 50 frames
            if self.frame_count % 50 == 0:
                self._print_status()

            # 9. Maintain poll interval
            elapsed = time.time() - loop_start
            if elapsed < poll_interval:
                time.sleep(poll_interval - elapsed)

    def _execute_action(self, action: BotAction):
        """Execute a decided action on the device."""
        if action.description:
            self.logger.debug(action.description)

        if action.action == Action.TAP:
            self.device.tap(action.x, action.y)
        elif action.action == Action.SWIPE:
            self.device.swipe(action.x, action.y, action.x2, action.y2)
        elif action.action == Action.LONG_PRESS:
            self.device.long_press(action.x, action.y, action.duration)
        elif action.action == Action.WAIT:
            time.sleep(action.duration)
        # Action.NONE = do nothing

    def _print_status(self):
        """Print periodic status update."""
        stats = self.logic.get_stats()
        runtime = datetime.now() - self.start_time
        hours, remainder = divmod(int(runtime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        self.logger.info(
            f"--- Status [{hours:02d}:{minutes:02d}:{seconds:02d}] ---  "
            f"Chapter: {stats['chapter']} | "
            f"Levels done: {stats['levels_completed']} | "
            f"Stars: {stats['total_stars']} | "
            f"Fails: {stats['levels_failed']} | "
            f"Frames: {self.frame_count}"
        )

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        self.logger.info("\nStopping bot...")
        self.running = False

    def _shutdown(self):
        """Clean shutdown with final stats."""
        self.logger.info("\n" + "=" * 50)
        self.logger.info("  BOT SESSION COMPLETE")
        self.logger.info("=" * 50)

        if self.start_time:
            runtime = datetime.now() - self.start_time
            self.logger.info(f"Runtime: {runtime}")

        stats = self.logic.get_stats()
        self.logger.info(f"Chapters progressed: {stats['chapter']}")
        self.logger.info(f"Levels completed:    {stats['levels_completed']}")
        self.logger.info(f"Total stars:         {stats['total_stars']}")
        self.logger.info(f"Levels failed:       {stats['levels_failed']}")
        self.logger.info(f"Frames processed:    {self.frame_count}")
        self.logger.info("=" * 50)


# ----------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------

def load_config(path: str) -> dict:
    """Load and validate configuration."""
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def main():
    parser = argparse.ArgumentParser(
        description="Domino Dreams iOS Bot - Automated game player"
    )
    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="Run calibration mode (take screenshot and analyze)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze screen but don't send any taps"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose/debug logging"
    )
    args = parser.parse_args()

    # Resolve config path
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(os.path.dirname(__file__), config_path)

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        print("Run from the domino-dreams-bot directory or specify --config path")
        sys.exit(1)

    config = load_config(config_path)
    verbose = args.verbose or config["bot"].get("verbose", False)
    setup_logging(verbose)

    if args.calibrate:
        device = iOSDevice(config)
        if device.connect():
            run_calibration(device, config)
        else:
            print("Failed to connect to device.")
            sys.exit(1)
    else:
        bot = DominoDreamsBot(config, dry_run=args.dry_run)
        bot.start()


if __name__ == "__main__":
    main()

"""
iOS Device Controller
Handles connecting to an iPhone over USB, taking screenshots,
and sending touch/swipe events using pymobiledevice3.
"""

import io
import time
import logging
import subprocess
import struct
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image
import numpy as np

logger = logging.getLogger("domino_bot.device")


class iOSDevice:
    """Manages connection to an iPhone and provides screen capture + touch input."""

    def __init__(self, config: dict):
        self.config = config
        self.screen_width = config["device"]["screen_width"]
        self.screen_height = config["device"]["screen_height"]
        self.scale_factor = config["device"]["scale_factor"]
        self.tap_delay = config["timing"]["tap_delay"]
        self.swipe_delay = config["timing"]["swipe_delay"]
        self._device_udid: Optional[str] = None
        self._connected = False

    def connect(self) -> bool:
        """Discover and connect to an iOS device over USB."""
        logger.info("Searching for connected iOS devices...")
        try:
            # Use pymobiledevice3 CLI to list devices
            result = subprocess.run(
                ["pymobiledevice3", "usbmux", "list", "--no-color"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                logger.error(f"Failed to list devices: {result.stderr}")
                return False

            output = result.stdout.strip()
            if not output or "no devices" in output.lower():
                logger.error(
                    "No iOS devices found. Make sure your iPhone is:\n"
                    "  1. Connected via USB\n"
                    "  2. Unlocked\n"
                    "  3. Trusted (tap 'Trust' on the popup)\n"
                    "  4. Developer mode enabled (Settings > Privacy > Developer Mode)"
                )
                return False

            # Parse UDID from output
            for line in output.split("\n"):
                line = line.strip()
                if line and len(line) >= 20 and not line.startswith(("-", "=", "[")):
                    self._device_udid = line.split()[0] if " " in line else line
                    break

            if not self._device_udid:
                # Try alternate parse - pymobiledevice3 may output JSON-like
                import json
                try:
                    devices = json.loads(output)
                    if isinstance(devices, list) and len(devices) > 0:
                        self._device_udid = devices[0].get("UniqueDeviceID") or devices[0].get("udid") or devices[0].get("UDID")
                except (json.JSONDecodeError, KeyError, IndexError):
                    pass

            if self._device_udid:
                logger.info(f"Connected to device: {self._device_udid}")
                self._connected = True
                return True
            else:
                logger.error("Could not parse device UDID from output.")
                logger.debug(f"Raw output: {output}")
                return False

        except FileNotFoundError:
            logger.error(
                "pymobiledevice3 not found. Install it with:\n"
                "  pip install pymobiledevice3"
            )
            return False
        except subprocess.TimeoutExpired:
            logger.error("Timed out searching for devices.")
            return False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def screenshot(self) -> Optional[np.ndarray]:
        """
        Capture a screenshot from the iOS device.
        Returns an OpenCV-compatible BGR numpy array, or None on failure.
        """
        if not self._connected:
            logger.error("Not connected to a device.")
            return None

        try:
            # pymobiledevice3 screenshot command outputs PNG to stdout
            cmd = ["pymobiledevice3", "developer", "dvt", "screenshot", "/dev/stdout"]
            if self._device_udid:
                cmd.extend(["--udid", self._device_udid])

            result = subprocess.run(
                cmd, capture_output=True, timeout=10
            )

            if result.returncode != 0:
                # Fallback: try the lockdown-based screenshot method
                return self._screenshot_fallback()

            # Convert PNG bytes to numpy array
            img = Image.open(io.BytesIO(result.stdout))
            img_array = np.array(img)

            # Convert RGB(A) to BGR for OpenCV
            if img_array.shape[2] == 4:
                img_bgr = img_array[:, :, [2, 1, 0]]  # RGBA -> BGR
            else:
                img_bgr = img_array[:, :, [2, 1, 0]]  # RGB -> BGR

            return img_bgr

        except subprocess.TimeoutExpired:
            logger.warning("Screenshot timed out, retrying...")
            return self._screenshot_fallback()
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return self._screenshot_fallback()

    def _screenshot_fallback(self) -> Optional[np.ndarray]:
        """Fallback screenshot method using alternate pymobiledevice3 commands."""
        try:
            # Try saving to a temp file instead
            tmp_path = "/tmp/domino_bot_screenshot.png"
            cmd = ["pymobiledevice3", "developer", "dvt", "screenshot", tmp_path]
            if self._device_udid:
                cmd.extend(["--udid", self._device_udid])

            result = subprocess.run(cmd, capture_output=True, timeout=15)

            if result.returncode != 0:
                # Try mount-based approach
                cmd2 = ["pymobiledevice3", "developer", "screenshot", tmp_path]
                if self._device_udid:
                    cmd2.extend(["--udid", self._device_udid])
                result = subprocess.run(cmd2, capture_output=True, timeout=15)

            if result.returncode == 0 and Path(tmp_path).exists():
                img = Image.open(tmp_path)
                img_array = np.array(img)
                if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
                    return img_array[:, :, [2, 1, 0]]
                return img_array

            logger.error(
                "Screenshot fallback also failed. Ensure developer services are available:\n"
                "  pymobiledevice3 developer dvt ls /\n"
                "If that fails, you may need to mount the developer disk image first."
            )
            return None

        except Exception as e:
            logger.error(f"Screenshot fallback failed: {e}")
            return None

    def tap(self, x: int, y: int):
        """
        Simulate a tap at the given (x, y) coordinates.
        Coordinates are in screen points (not pixels).
        """
        if not self._connected:
            logger.error("Not connected to a device.")
            return

        logger.debug(f"Tap at ({x}, {y})")
        try:
            cmd = [
                "pymobiledevice3", "developer", "dvt", "simulate-location",
                "play", str(x), str(y)
            ]
            # The above is for location - for touch we use accessibility or hid
            # Use the HID (Human Interface Device) approach
            self._send_touch_event(x, y)
        except Exception as e:
            logger.error(f"Tap failed: {e}")

        time.sleep(self.tap_delay)

    def _send_touch_event(self, x: int, y: int, duration: float = 0.05):
        """Send a touch event via pymobiledevice3 accessibility or HID."""
        try:
            # Method 1: Using pymobiledevice3 developer dvt accessibility
            cmd = [
                "pymobiledevice3", "developer", "dvt", "accessibility",
                "run-action", "tap", str(x), str(y)
            ]
            if self._device_udid:
                cmd.extend(["--udid", self._device_udid])

            result = subprocess.run(cmd, capture_output=True, timeout=5)
            if result.returncode == 0:
                return

            # Method 2: Direct simulate touch via subprocess
            # pymobiledevice3 has a 'simulate' subcommand in newer versions
            cmd2 = [
                "pymobiledevice3", "developer", "simulate-touch",
                "tap", str(x), str(y)
            ]
            if self._device_udid:
                cmd2.extend(["--udid", self._device_udid])

            result = subprocess.run(cmd2, capture_output=True, timeout=5)
            if result.returncode == 0:
                return

            # Method 3: Use Python API directly
            self._send_touch_via_api(x, y, duration)

        except Exception as e:
            logger.error(f"Touch event failed: {e}")
            self._send_touch_via_api(x, y, duration)

    def _send_touch_via_api(self, x: int, y: int, duration: float = 0.05):
        """Send touch event using pymobiledevice3 Python API."""
        try:
            from pymobiledevice3.lockdown import create_using_usbmux
            from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
            from pymobiledevice3.services.dvt.instruments.device_info import DeviceInfo

            lockdown = create_using_usbmux(serial=self._device_udid)

            # Use the remote HID simulation
            with DvtSecureSocketProxyService(lockdown=lockdown) as dvt:
                # Simulate a tap using the HID channel
                # Touch down
                dvt.send_message(
                    "_WDAutomation",
                    "tap",
                    {"x": x, "y": y, "duration": duration}
                )
        except ImportError:
            logger.warning("Could not import pymobiledevice3 API modules")
        except Exception as e:
            logger.debug(f"API touch event: {e}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.3):
        """
        Simulate a swipe gesture from (x1, y1) to (x2, y2).
        """
        if not self._connected:
            return

        logger.debug(f"Swipe from ({x1},{y1}) to ({x2},{y2})")
        try:
            cmd = [
                "pymobiledevice3", "developer", "dvt", "accessibility",
                "run-action", "swipe",
                str(x1), str(y1), str(x2), str(y2),
                "--duration", str(duration)
            ]
            if self._device_udid:
                cmd.extend(["--udid", self._device_udid])

            subprocess.run(cmd, capture_output=True, timeout=10)
        except Exception as e:
            logger.error(f"Swipe failed: {e}")

        time.sleep(self.swipe_delay)

    def long_press(self, x: int, y: int, duration: float = 1.0):
        """Simulate a long press at (x, y)."""
        if not self._connected:
            return

        logger.debug(f"Long press at ({x}, {y}) for {duration}s")
        self._send_touch_event(x, y, duration=duration)
        time.sleep(duration + self.tap_delay)

    def save_screenshot(self, path: str, frame: Optional[np.ndarray] = None):
        """Save a screenshot to disk for debugging."""
        if frame is None:
            frame = self.screenshot()
        if frame is not None:
            # Convert BGR back to RGB for saving
            img = Image.fromarray(frame[:, :, [2, 1, 0]])
            img.save(path)
            logger.debug(f"Screenshot saved: {path}")

"""
Game Vision Module
Uses OpenCV to detect game elements on screen: dominoes, buttons,
popups, menus, progress indicators, and game state.
"""

import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger("domino_bot.vision")


class GameScreen(Enum):
    """Detected screen states in Domino Dreams."""
    UNKNOWN = auto()
    HOME_MENU = auto()
    CHAPTER_MAP = auto()
    LEVEL_SELECT = auto()
    GAMEPLAY = auto()
    LEVEL_COMPLETE = auto()
    LEVEL_FAILED = auto()
    REWARD_POPUP = auto()
    CHAPTER_COMPLETE = auto()
    LOADING = auto()
    POPUP_DIALOG = auto()
    SHOP = auto()
    SETTINGS = auto()
    OUT_OF_LIVES = auto()
    BUILDING_SCENE = auto()


@dataclass
class Point:
    x: int
    y: int


@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> Point:
        return Point(self.x + self.w // 2, self.y + self.h // 2)


@dataclass
class Domino:
    """A detected domino piece on the game board."""
    bbox: BoundingBox
    top_value: int = 0  # dots on top half (0-6)
    bottom_value: int = 0  # dots on bottom half (0-6)
    is_playable: bool = False
    is_highlighted: bool = False


@dataclass
class GameState:
    """Complete detected state of the current game screen."""
    screen: GameScreen = GameScreen.UNKNOWN
    dominoes: List[Domino] = field(default_factory=list)
    play_button: Optional[BoundingBox] = None
    continue_button: Optional[BoundingBox] = None
    close_button: Optional[BoundingBox] = None
    collect_button: Optional[BoundingBox] = None
    retry_button: Optional[BoundingBox] = None
    next_button: Optional[BoundingBox] = None
    tap_targets: List[BoundingBox] = field(default_factory=list)
    score: int = 0
    moves_remaining: int = -1
    stars_earned: int = 0
    is_animating: bool = False
    chain_active: bool = False
    board_region: Optional[BoundingBox] = None


class GameVision:
    """Computer vision engine for detecting Domino Dreams game elements."""

    def __init__(self, config: dict):
        self.config = config
        self.det = config["detection"]
        self.colors = config["colors"]
        self.match_threshold = self.det["match_threshold"]
        self.color_tolerance = self.det["color_tolerance"]
        self.min_domino_area = self.det["min_domino_area"]
        self.max_domino_area = self.det["max_domino_area"]

        # Screen dimensions for region calculations
        sw = config["device"]["screen_width"] * config["device"]["scale_factor"]
        sh = config["device"]["screen_height"] * config["device"]["scale_factor"]
        self.screen_w = sw
        self.screen_h = sh
        self.scale = config["device"]["scale_factor"]

        # Define screen regions (in pixel coordinates)
        self._regions = {
            "top_bar": (0, 0, sw, int(sh * 0.12)),
            "board": (0, int(sh * 0.12), sw, int(sh * 0.75)),
            "bottom_bar": (0, int(sh * 0.82), sw, int(sh * 0.18)),
            "center": (int(sw * 0.15), int(sh * 0.25), int(sw * 0.7), int(sh * 0.5)),
            "center_button": (int(sw * 0.2), int(sh * 0.55), int(sw * 0.6), int(sh * 0.15)),
        }

        self._prev_frame = None
        self._templates_loaded = False

    def analyze(self, frame: np.ndarray) -> GameState:
        """
        Analyze a screenshot and return the detected game state.
        This is the main entry point called every frame.
        """
        if frame is None:
            return GameState(screen=GameScreen.UNKNOWN)

        state = GameState()

        # Step 1: Check if screen is animating (compare to previous frame)
        state.is_animating = self._check_animating(frame)
        self._prev_frame = frame.copy()

        if state.is_animating:
            state.screen = GameScreen.LOADING
            return state

        # Step 2: Detect which screen we're on
        state.screen = self._detect_screen(frame)

        # Step 3: Based on screen, detect relevant elements
        if state.screen == GameScreen.GAMEPLAY:
            state.board_region = self._find_board_region(frame)
            state.dominoes = self._detect_dominoes(frame)
            state.tap_targets = self._find_tap_targets(frame)
            state.moves_remaining = self._detect_moves(frame)
            state.chain_active = self._detect_chain(frame)
        elif state.screen == GameScreen.LEVEL_COMPLETE:
            state.continue_button = self._find_button_by_color(frame, "play_button_green")
            state.collect_button = self._find_button_by_color(frame, "reward_gold")
            state.stars_earned = self._detect_stars(frame)
        elif state.screen == GameScreen.LEVEL_FAILED:
            state.retry_button = self._find_button_by_color(frame, "play_button_green")
            state.close_button = self._find_x_button(frame)
        elif state.screen == GameScreen.CHAPTER_COMPLETE:
            state.continue_button = self._find_button_by_color(frame, "play_button_green")
            state.collect_button = self._find_button_by_color(frame, "reward_gold")
        elif state.screen in (GameScreen.HOME_MENU, GameScreen.CHAPTER_MAP, GameScreen.LEVEL_SELECT):
            state.play_button = self._find_button_by_color(frame, "play_button_green")
            if state.play_button is None:
                state.play_button = self._find_button_by_color(frame, "play_button_orange")
        elif state.screen == GameScreen.REWARD_POPUP:
            state.collect_button = self._find_button_by_color(frame, "play_button_green")
            state.close_button = self._find_x_button(frame)
        elif state.screen == GameScreen.POPUP_DIALOG:
            state.close_button = self._find_x_button(frame)
            state.continue_button = self._find_button_by_color(frame, "play_button_green")
        elif state.screen == GameScreen.OUT_OF_LIVES:
            state.close_button = self._find_x_button(frame)
        elif state.screen == GameScreen.BUILDING_SCENE:
            state.tap_targets = self._find_glowing_elements(frame)
            state.continue_button = self._find_button_by_color(frame, "play_button_green")

        # Always look for generic tap/close targets as fallback
        if not any([state.play_button, state.continue_button, state.close_button,
                     state.collect_button, state.retry_button, state.tap_targets]):
            state.tap_targets = self._find_any_buttons(frame)

        return state

    def _check_animating(self, frame: np.ndarray) -> bool:
        """Check if the screen is still animating by comparing frames."""
        if self._prev_frame is None:
            return False

        if frame.shape != self._prev_frame.shape:
            return False

        # Compare a central region to avoid UI element flicker
        h, w = frame.shape[:2]
        roi_curr = frame[h // 4:3 * h // 4, w // 4:3 * w // 4]
        roi_prev = self._prev_frame[h // 4:3 * h // 4, w // 4:3 * w // 4]

        diff = cv2.absdiff(roi_curr, roi_prev)
        mean_diff = np.mean(diff)

        # If more than 15% of pixels changed significantly, still animating
        return mean_diff > 12.0

    def _detect_screen(self, frame: np.ndarray) -> GameScreen:
        """Determine which game screen is currently displayed."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w = frame.shape[:2]

        # Check for dark overlay (popup/dialog)
        center_region = frame[h // 3:2 * h // 3, w // 4:3 * w // 4]
        edge_region = np.vstack([frame[:h // 6, :], frame[5 * h // 6:, :]])
        center_brightness = np.mean(center_region)
        edge_brightness = np.mean(edge_region)

        has_dark_overlay = edge_brightness < 60 and center_brightness > edge_brightness + 40

        # Detect specific text/UI elements by looking for characteristic patterns
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Check bottom region for gameplay elements (move counter, score)
        bottom_strip = gray[int(h * 0.88):, :]
        bottom_white = np.sum(bottom_strip > 200) / bottom_strip.size

        # Check top region for score/level indicators
        top_strip = gray[:int(h * 0.1), :]
        top_activity = np.std(top_strip)

        # Check for green play button (prominent on many screens)
        green_mask = self._color_mask(hsv, "play_button_green")
        green_area = np.sum(green_mask > 0)

        # Check for reward/gold colors
        gold_mask = self._color_mask(hsv, "reward_gold")
        gold_area = np.sum(gold_mask > 0)

        # Check for domino-like white rectangular objects in the middle
        mid_region = gray[int(h * 0.15):int(h * 0.8), int(w * 0.05):int(w * 0.95)]
        _, white_thresh = cv2.threshold(mid_region, 220, 255, cv2.THRESH_BINARY)
        white_contours, _ = cv2.findContours(
            white_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        domino_like_objects = sum(
            1 for c in white_contours
            if self.min_domino_area < cv2.contourArea(c) < self.max_domino_area
        )

        # Decision logic
        if has_dark_overlay:
            if gold_area > 5000:
                return GameScreen.REWARD_POPUP
            elif green_area > 3000:
                # Could be level complete, failed, or generic popup
                # Check for star-like shapes
                stars = self._detect_stars(frame)
                if stars > 0:
                    return GameScreen.LEVEL_COMPLETE
                else:
                    return GameScreen.POPUP_DIALOG
            else:
                # Check for X button suggesting a closeable popup
                if self._find_x_button(frame) is not None:
                    return GameScreen.POPUP_DIALOG
                return GameScreen.LOADING

        if domino_like_objects >= 3:
            return GameScreen.GAMEPLAY

        # Check for building/decoration scene (colorful, interactive elements)
        color_variance = np.std(hsv[:, :, 0])
        if color_variance > 40 and green_area > 2000:
            # Could be chapter map or building scene
            if bottom_white > 0.3:
                return GameScreen.CHAPTER_MAP
            return GameScreen.BUILDING_SCENE

        if green_area > 5000 and top_activity > 40:
            return GameScreen.LEVEL_SELECT

        if green_area > 8000:
            return GameScreen.HOME_MENU

        # Check for "out of lives" - typically has a heart icon
        red_mask = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
        red_area = np.sum(red_mask > 0)
        if red_area > 3000 and has_dark_overlay:
            return GameScreen.OUT_OF_LIVES

        return GameScreen.UNKNOWN

    def _color_mask(self, hsv: np.ndarray, color_name: str) -> np.ndarray:
        """Create a binary mask for a named color from config."""
        c = self.colors[color_name]
        lower = np.array(c[:3])
        upper = np.array(c[3:])
        return cv2.inRange(hsv, lower, upper)

    def _find_board_region(self, frame: np.ndarray) -> Optional[BoundingBox]:
        """Find the main game board area."""
        h, w = frame.shape[:2]
        # The board is typically in the middle 70% of the screen
        return BoundingBox(
            x=int(w * 0.03),
            y=int(h * 0.12),
            w=int(w * 0.94),
            h=int(h * 0.68)
        )

    def _detect_dominoes(self, frame: np.ndarray) -> List[Domino]:
        """Detect domino pieces on the game board."""
        dominoes = []
        h, w = frame.shape[:2]

        # Focus on the board region
        board_y1 = int(h * 0.12)
        board_y2 = int(h * 0.80)
        board_x1 = int(w * 0.03)
        board_x2 = int(w * 0.97)
        board = frame[board_y1:board_y2, board_x1:board_x2]

        # Convert to HSV for color detection
        hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

        # Dominoes are typically white/light colored rectangles
        # with colored dots or dark dividing lines
        _, white_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Also detect colored dominoes (game uses various colors)
        bright_mask = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 80, 255]))
        combined = cv2.bitwise_or(white_mask, bright_mask)

        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
        combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if not (self.min_domino_area < area < self.max_domino_area):
                continue

            # Check aspect ratio - dominoes are roughly rectangular
            rect = cv2.minAreaRect(contour)
            box_w, box_h = rect[1]
            if box_w == 0 or box_h == 0:
                continue
            aspect = max(box_w, box_h) / min(box_w, box_h)
            if aspect > 4.0:
                continue  # Too elongated

            x, y, bw, bh = cv2.boundingRect(contour)

            # Adjust coordinates back to full frame
            abs_x = x + board_x1
            abs_y = y + board_y1

            # Convert pixel coords to screen points
            pt_x = abs_x // self.scale
            pt_y = abs_y // self.scale
            pt_w = bw // self.scale
            pt_h = bh // self.scale

            bbox = BoundingBox(pt_x, pt_y, pt_w, pt_h)

            # Count dots in top and bottom halves
            domino_roi = gray[y:y + bh, x:x + bw] if bh > 0 and bw > 0 else None
            top_val, bottom_val = 0, 0
            if domino_roi is not None and domino_roi.size > 0:
                top_val = self._count_dots(domino_roi[:bh // 2, :])
                bottom_val = self._count_dots(domino_roi[bh // 2:, :])

            # Check if domino is highlighted (glowing/pulsing = playable)
            is_highlighted = self._is_highlighted(
                frame[abs_y:abs_y + bh, abs_x:abs_x + bw]
            )

            dominoes.append(Domino(
                bbox=bbox,
                top_value=top_val,
                bottom_value=bottom_val,
                is_playable=True,  # Assume playable, refined in game logic
                is_highlighted=is_highlighted
            ))

        logger.debug(f"Detected {len(dominoes)} dominoes")
        return dominoes

    def _count_dots(self, roi: np.ndarray) -> int:
        """Count the number of dots in a domino half."""
        if roi is None or roi.size == 0:
            return 0

        # Dots are dark circles on light background
        _, dark_mask = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY_INV)

        # Find circular blobs
        contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        dot_count = 0
        min_dot_area = roi.size * 0.005  # Minimum 0.5% of ROI
        max_dot_area = roi.size * 0.15  # Maximum 15% of ROI

        for c in contours:
            area = cv2.contourArea(c)
            if min_dot_area < area < max_dot_area:
                # Check circularity
                perimeter = cv2.arcLength(c, True)
                if perimeter > 0:
                    circularity = 4 * 3.14159 * area / (perimeter * perimeter)
                    if circularity > 0.4:  # Reasonably circular
                        dot_count += 1

        return min(dot_count, 6)  # Cap at 6

    def _is_highlighted(self, roi: np.ndarray) -> bool:
        """Check if a domino region is highlighted/glowing."""
        if roi is None or roi.size == 0:
            return False

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # Highlighted dominoes often have higher saturation or brightness
        avg_sat = np.mean(hsv[:, :, 1])
        avg_val = np.mean(hsv[:, :, 2])

        # A glow typically shows high value and moderate saturation
        return avg_val > 200 and avg_sat > 30

    def _find_tap_targets(self, frame: np.ndarray) -> List[BoundingBox]:
        """
        Find tappable/interactive elements during gameplay.
        In Domino Dreams, players tap domino pieces to trigger chain reactions.
        """
        targets = []
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Look for glowing/pulsing elements (typically brighter, saturated)
        # These are the dominoes you're supposed to tap
        glow_mask = cv2.inRange(
            hsv,
            np.array([0, 40, 220]),
            np.array([180, 255, 255])
        )

        # Focus on board region
        board_mask = np.zeros_like(glow_mask)
        board_y1 = int(h * 0.12)
        board_y2 = int(h * 0.80)
        board_mask[board_y1:board_y2, :] = 255
        glow_mask = cv2.bitwise_and(glow_mask, board_mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        glow_mask = cv2.morphologyEx(glow_mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(glow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_domino_area:
                continue
            x, y, bw, bh = cv2.boundingRect(c)
            targets.append(BoundingBox(
                x=x // self.scale,
                y=y // self.scale,
                w=bw // self.scale,
                h=bh // self.scale
            ))

        return targets

    def _find_button_by_color(self, frame: np.ndarray, color_name: str) -> Optional[BoundingBox]:
        """Find a button matching a specific color profile."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = self._color_mask(hsv, color_name)

        # Clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest matching region that looks like a button
        best = None
        best_area = 0

        for c in contours:
            area = cv2.contourArea(c)
            if area < 2000:  # Too small to be a button
                continue
            if area > best_area:
                x, y, bw, bh = cv2.boundingRect(c)
                # Buttons are wider than tall
                if bw > bh * 0.5:
                    best = BoundingBox(
                        x=x // self.scale,
                        y=y // self.scale,
                        w=bw // self.scale,
                        h=bh // self.scale
                    )
                    best_area = area

        return best

    def _find_x_button(self, frame: np.ndarray) -> Optional[BoundingBox]:
        """Find an X/close button, typically in the top-right of a popup."""
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # X buttons are usually in the top-right quadrant of popups
        # Scan the upper portion of the frame
        search_region = gray[:int(h * 0.4), int(w * 0.5):]

        # X buttons are often circular with an X pattern inside
        circles = cv2.HoughCircles(
            search_region, cv2.HOUGH_GRADIENT, 1, 30,
            param1=100, param2=30, minRadius=10, maxRadius=40
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for cx, cy, r in circles[0]:
                abs_x = int(cx + w * 0.5)
                abs_y = int(cy)
                return BoundingBox(
                    x=(abs_x - r) // self.scale,
                    y=(abs_y - r) // self.scale,
                    w=(2 * r) // self.scale,
                    h=(2 * r) // self.scale
                )

        # Fallback: look for small dark circles in corners of detected popups
        _, dark_mask = cv2.threshold(gray[:int(h * 0.5), :], 80, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            area = cv2.contourArea(c)
            if 200 < area < 5000:
                perimeter = cv2.arcLength(c, True)
                if perimeter > 0:
                    circularity = 4 * 3.14159 * area / (perimeter * perimeter)
                    if circularity > 0.6:
                        x, y, bw, bh = cv2.boundingRect(c)
                        if x > w * 0.5:  # Right side
                            return BoundingBox(
                                x=x // self.scale,
                                y=y // self.scale,
                                w=bw // self.scale,
                                h=bh // self.scale
                            )

        return None

    def _find_glowing_elements(self, frame: np.ndarray) -> List[BoundingBox]:
        """Find glowing/interactive elements in building scenes."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        targets = []

        # Glowing elements have high brightness and often a colored outline
        glow = cv2.inRange(hsv, np.array([0, 50, 230]), np.array([180, 255, 255]))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        glow = cv2.morphologyEx(glow, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(glow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if 1000 < area < 100000:
                x, y, bw, bh = cv2.boundingRect(c)
                targets.append(BoundingBox(
                    x=x // self.scale,
                    y=y // self.scale,
                    w=bw // self.scale,
                    h=bh // self.scale
                ))

        return targets

    def _find_any_buttons(self, frame: np.ndarray) -> List[BoundingBox]:
        """Last resort: find anything that looks like a tappable button."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w = frame.shape[:2]
        targets = []

        # Look for saturated, bright rectangular regions (buttons)
        sat_mask = cv2.inRange(hsv, np.array([0, 80, 150]), np.array([180, 255, 255]))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))
        sat_mask = cv2.morphologyEx(sat_mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(sat_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if 3000 < area < 80000:
                x, y, bw, bh = cv2.boundingRect(c)
                # Button-like aspect ratio
                if bw > bh * 1.2 and bh > 20:
                    targets.append(BoundingBox(
                        x=x // self.scale,
                        y=y // self.scale,
                        w=bw // self.scale,
                        h=bh // self.scale
                    ))

        return targets

    def _detect_stars(self, frame: np.ndarray) -> int:
        """Detect number of stars earned on level complete screen."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w = frame.shape[:2]

        # Stars are golden/yellow, typically in the upper-center of the popup
        star_region = hsv[int(h * 0.15):int(h * 0.45), int(w * 0.15):int(w * 0.85)]
        gold_mask = cv2.inRange(star_region, np.array([15, 100, 150]), np.array([35, 255, 255]))

        # Count distinct gold blobs
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        gold_mask = cv2.morphologyEx(gold_mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(gold_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        star_count = sum(1 for c in contours if cv2.contourArea(c) > 500)
        return min(star_count, 3)

    def _detect_moves(self, frame: np.ndarray) -> int:
        """Detect remaining moves counter (returns -1 if not found)."""
        # This would ideally use OCR - for now, return -1 (unknown)
        # The bot doesn't strictly need this since it plays by visual cues
        return -1

    def _detect_chain(self, frame: np.ndarray) -> bool:
        """Detect if a domino chain reaction is currently in progress."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w = frame.shape[:2]

        # During chain reactions, there are usually bright particle effects
        board_region = hsv[int(h * 0.15):int(h * 0.8), :]
        bright_count = np.sum(board_region[:, :, 2] > 240)
        total_pixels = board_region[:, :, 2].size

        # If more than 5% of the board is extremely bright, likely a chain
        return (bright_count / total_pixels) > 0.05

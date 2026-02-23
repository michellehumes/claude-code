"""
Game Logic & Decision Engine
Decides what action to take based on the detected game state.
Handles gameplay strategy, popup dismissal, and chapter navigation.
"""

import logging
import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple

from game_vision import (
    GameScreen, GameState, Domino, BoundingBox, Point
)

logger = logging.getLogger("domino_bot.logic")


class Action(Enum):
    """Bot actions."""
    TAP = auto()
    SWIPE = auto()
    LONG_PRESS = auto()
    WAIT = auto()
    NONE = auto()


@dataclass
class BotAction:
    """A concrete action for the bot to perform."""
    action: Action
    x: int = 0
    y: int = 0
    x2: int = 0  # For swipe end
    y2: int = 0  # For swipe end
    duration: float = 0.0
    description: str = ""


class GameLogic:
    """
    Decision engine that converts game state into bot actions.
    Implements the strategy for playing Domino Dreams levels.
    """

    def __init__(self, config: dict):
        self.config = config
        self.screen_w = config["device"]["screen_width"]
        self.screen_h = config["device"]["screen_height"]
        self.auto_collect = config["bot"]["auto_collect_rewards"]
        self.auto_dismiss = config["bot"]["auto_dismiss_popups"]

        # Track state across frames
        self.current_chapter = 0
        self.current_level = 0
        self.levels_completed = 0
        self.levels_failed = 0
        self.total_stars = 0
        self.consecutive_fails = 0
        self.stuck_count = 0
        self.last_screen = GameScreen.UNKNOWN
        self.same_screen_count = 0
        self.last_action_time = 0

    def decide(self, state: GameState) -> BotAction:
        """
        Given the current game state, decide the next action.
        This is the main brain of the bot.
        """
        # Track if we're stuck on the same screen
        if state.screen == self.last_screen:
            self.same_screen_count += 1
        else:
            self.same_screen_count = 0
        self.last_screen = state.screen

        # If stuck on the same screen for too long, try recovery
        if self.same_screen_count > 15:
            logger.warning(f"Stuck on {state.screen.name} for {self.same_screen_count} frames")
            return self._recover_stuck(state)

        # Route to screen-specific handlers
        handlers = {
            GameScreen.GAMEPLAY: self._handle_gameplay,
            GameScreen.LEVEL_COMPLETE: self._handle_level_complete,
            GameScreen.LEVEL_FAILED: self._handle_level_failed,
            GameScreen.CHAPTER_COMPLETE: self._handle_chapter_complete,
            GameScreen.HOME_MENU: self._handle_menu,
            GameScreen.CHAPTER_MAP: self._handle_chapter_map,
            GameScreen.LEVEL_SELECT: self._handle_level_select,
            GameScreen.REWARD_POPUP: self._handle_reward_popup,
            GameScreen.POPUP_DIALOG: self._handle_popup,
            GameScreen.OUT_OF_LIVES: self._handle_out_of_lives,
            GameScreen.BUILDING_SCENE: self._handle_building_scene,
            GameScreen.LOADING: self._handle_loading,
            GameScreen.UNKNOWN: self._handle_unknown,
        }

        handler = handlers.get(state.screen, self._handle_unknown)
        action = handler(state)

        self.last_action_time = time.time()
        return action

    # ----------------------------------------------------------------
    # Screen-specific handlers
    # ----------------------------------------------------------------

    def _handle_gameplay(self, state: GameState) -> BotAction:
        """
        Handle the main gameplay screen.
        Strategy: Tap highlighted/playable dominoes to start chain reactions.
        """
        # If a chain is active, wait for it to finish
        if state.chain_active:
            return BotAction(
                action=Action.WAIT,
                duration=0.5,
                description="Waiting for chain reaction to finish"
            )

        # If the screen is animating, wait
        if state.is_animating:
            return BotAction(
                action=Action.WAIT,
                duration=0.3,
                description="Waiting for animation"
            )

        # Priority 1: Tap highlighted dominoes (the game hints at these)
        highlighted = [d for d in state.dominoes if d.is_highlighted]
        if highlighted:
            target = self._pick_best_domino(highlighted)
            center = target.bbox.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description=f"Tapping highlighted domino at ({center.x}, {center.y})"
            )

        # Priority 2: Tap detected tap targets (glowing elements)
        if state.tap_targets:
            target = self._pick_best_target(state.tap_targets)
            center = target.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description=f"Tapping target at ({center.x}, {center.y})"
            )

        # Priority 3: Tap any playable domino, prioritizing edges and corners
        playable = [d for d in state.dominoes if d.is_playable]
        if playable:
            target = self._pick_strategic_domino(playable, state)
            center = target.bbox.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description=f"Tapping domino [{target.top_value}|{target.bottom_value}] at ({center.x}, {center.y})"
            )

        # Priority 4: If no dominoes detected, tap the center of the board
        if state.board_region:
            center = state.board_region.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="No targets found - tapping board center"
            )

        # Fallback: tap center of screen
        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=self.screen_h // 2,
            description="Fallback: tapping screen center"
        )

    def _handle_level_complete(self, state: GameState) -> BotAction:
        """Handle the level complete screen."""
        self.levels_completed += 1
        self.consecutive_fails = 0
        self.total_stars += state.stars_earned
        self.current_level += 1

        logger.info(
            f"Level complete! Stars: {state.stars_earned} | "
            f"Total completed: {self.levels_completed}"
        )

        # Tap collect/continue button
        if state.collect_button and self.auto_collect:
            center = state.collect_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Collecting rewards"
            )

        if state.continue_button:
            center = state.continue_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Continuing to next level"
            )

        # Tap center-bottom where continue usually is
        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.7),
            description="Tapping where continue button should be"
        )

    def _handle_level_failed(self, state: GameState) -> BotAction:
        """Handle level failed screen."""
        self.levels_failed += 1
        self.consecutive_fails += 1

        logger.info(
            f"Level failed (attempt {self.consecutive_fails}). "
            f"Total fails: {self.levels_failed}"
        )

        max_retries = self.config["bot"]["max_level_retries"]

        if self.consecutive_fails >= max_retries:
            logger.warning(
                f"Failed {self.consecutive_fails} times. "
                "Will try once more, then skip if possible."
            )

        # Tap retry button
        if state.retry_button:
            center = state.retry_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Retrying level"
            )

        if state.close_button:
            center = state.close_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Closing fail screen"
            )

        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.65),
            description="Tapping where retry button should be"
        )

    def _handle_chapter_complete(self, state: GameState) -> BotAction:
        """Handle chapter completion screen."""
        self.current_chapter += 1
        self.current_level = 0
        self.consecutive_fails = 0

        logger.info(f"Chapter {self.current_chapter} complete!")

        if state.collect_button:
            center = state.collect_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Collecting chapter rewards"
            )

        if state.continue_button:
            center = state.continue_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Continuing to next chapter"
            )

        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.7),
            description="Tapping to advance chapter"
        )

    def _handle_menu(self, state: GameState) -> BotAction:
        """Handle the home/main menu."""
        if state.play_button:
            center = state.play_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Tapping play button on main menu"
            )

        # Play button is usually center-bottom
        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.75),
            description="Tapping where play button should be"
        )

    def _handle_chapter_map(self, state: GameState) -> BotAction:
        """Handle the chapter/world map screen."""
        if state.play_button:
            center = state.play_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Tapping play on chapter map"
            )

        # Try tapping the next level marker (usually highlighted)
        if state.tap_targets:
            target = state.tap_targets[0]
            center = target.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Tapping next level on map"
            )

        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.6),
            description="Tapping center of chapter map"
        )

    def _handle_level_select(self, state: GameState) -> BotAction:
        """Handle level selection screen."""
        if state.play_button:
            center = state.play_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Starting level from selection screen"
            )

        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.7),
            description="Tapping where level start button should be"
        )

    def _handle_reward_popup(self, state: GameState) -> BotAction:
        """Handle reward collection popups."""
        if self.auto_collect and state.collect_button:
            center = state.collect_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Collecting reward"
            )

        if state.close_button:
            center = state.close_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Closing reward popup"
            )

        # Tap anywhere to dismiss
        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.8),
            description="Dismissing reward popup"
        )

    def _handle_popup(self, state: GameState) -> BotAction:
        """Handle generic popup dialogs."""
        if not self.auto_dismiss:
            return BotAction(action=Action.WAIT, duration=2.0,
                             description="Waiting (auto-dismiss disabled)")

        if state.close_button:
            center = state.close_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Closing popup"
            )

        if state.continue_button:
            center = state.continue_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Tapping continue on popup"
            )

        # Try tapping outside the popup to dismiss
        return BotAction(
            action=Action.TAP,
            x=20, y=int(self.screen_h * 0.1),
            description="Tapping outside popup to dismiss"
        )

    def _handle_out_of_lives(self, state: GameState) -> BotAction:
        """Handle the out-of-lives screen."""
        logger.warning("Out of lives! Closing dialog and waiting for refill...")

        if state.close_button:
            center = state.close_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Closing out-of-lives popup"
            )

        # Try the X button position (top-right of popup)
        return BotAction(
            action=Action.TAP,
            x=int(self.screen_w * 0.85),
            y=int(self.screen_h * 0.25),
            description="Trying to close lives popup"
        )

    def _handle_building_scene(self, state: GameState) -> BotAction:
        """
        Handle the building/decoration scenes between chapters.
        These are interactive scenes where you place items.
        """
        if state.tap_targets:
            target = state.tap_targets[0]
            center = target.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Tapping interactive building element"
            )

        if state.continue_button:
            center = state.continue_button.center
            return BotAction(
                action=Action.TAP,
                x=center.x, y=center.y,
                description="Continuing past building scene"
            )

        # Tap around to advance the scene
        return BotAction(
            action=Action.TAP,
            x=self.screen_w // 2,
            y=int(self.screen_h * 0.5),
            description="Tapping to advance building scene"
        )

    def _handle_loading(self, state: GameState) -> BotAction:
        """Handle loading screens - just wait."""
        return BotAction(
            action=Action.WAIT,
            duration=1.0,
            description="Waiting for loading"
        )

    def _handle_unknown(self, state: GameState) -> BotAction:
        """Handle unknown screens."""
        self.stuck_count += 1

        if self.stuck_count > 5:
            # Try various recovery taps
            return self._recover_stuck(state)

        return BotAction(
            action=Action.WAIT,
            duration=1.0,
            description="Unknown screen - waiting"
        )

    # ----------------------------------------------------------------
    # Strategy helpers
    # ----------------------------------------------------------------

    def _pick_best_domino(self, dominoes: List[Domino]) -> Domino:
        """Pick the best domino to tap from highlighted options."""
        if len(dominoes) == 1:
            return dominoes[0]

        # Prefer dominoes with higher values (more points)
        scored = [(d, d.top_value + d.bottom_value) for d in dominoes]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

    def _pick_best_target(self, targets: List[BoundingBox]) -> BoundingBox:
        """Pick the best tap target from a list of options."""
        if len(targets) == 1:
            return targets[0]

        # Prefer targets closer to the center of the board
        center_x = self.screen_w // 2
        center_y = int(self.screen_h * 0.45)

        def distance_to_center(bb):
            c = bb.center
            return ((c.x - center_x) ** 2 + (c.y - center_y) ** 2) ** 0.5

        targets.sort(key=distance_to_center)
        return targets[0]

    def _pick_strategic_domino(self, dominoes: List[Domino], state: GameState) -> Domino:
        """
        Pick a domino using a strategic approach.
        Strategy for Domino Dreams:
        - Prioritize dominoes that will trigger the longest chains
        - Corner and edge dominoes often create better chain reactions
        - Higher value dominoes score more points
        """
        if len(dominoes) == 1:
            return dominoes[0]

        scored_dominoes = []
        board_center_x = self.screen_w // 2
        board_center_y = int(self.screen_h * 0.45)

        for domino in dominoes:
            score = 0
            cx, cy = domino.bbox.center.x, domino.bbox.center.y

            # Value score: higher domino values = more points
            score += (domino.top_value + domino.bottom_value) * 10

            # Edge bonus: dominoes near edges often start longer chains
            edge_dist_x = min(cx, self.screen_w - cx)
            edge_dist_y = min(cy - int(self.screen_h * 0.12),
                              int(self.screen_h * 0.80) - cy)
            if edge_dist_x < self.screen_w * 0.15:
                score += 20
            if edge_dist_y < self.screen_h * 0.1:
                score += 20

            # Neighbor bonus: dominoes near other dominoes create chains
            for other in dominoes:
                if other is domino:
                    continue
                dist = (
                    (cx - other.bbox.center.x) ** 2 +
                    (cy - other.bbox.center.y) ** 2
                ) ** 0.5
                if dist < 80:  # Close neighbor
                    score += 15
                elif dist < 150:
                    score += 5

            # Highlighted bonus
            if domino.is_highlighted:
                score += 50

            # Small random factor to avoid getting stuck in loops
            score += random.randint(0, 10)

            scored_dominoes.append((domino, score))

        scored_dominoes.sort(key=lambda x: x[1], reverse=True)
        return scored_dominoes[0][0]

    def _recover_stuck(self, state: GameState) -> BotAction:
        """Try to recover when the bot is stuck."""
        self.same_screen_count = 0  # Reset counter

        recovery_positions = [
            # Tap various positions to try to unstick
            (self.screen_w // 2, int(self.screen_h * 0.5)),  # Center
            (self.screen_w // 2, int(self.screen_h * 0.75)),  # Bottom center
            (int(self.screen_w * 0.85), int(self.screen_h * 0.08)),  # Top right (X button)
            (self.screen_w // 2, int(self.screen_h * 0.9)),  # Very bottom
            (20, int(self.screen_h * 0.05)),  # Top left (back button)
        ]

        idx = self.stuck_count % len(recovery_positions)
        x, y = recovery_positions[idx]
        self.stuck_count += 1

        return BotAction(
            action=Action.TAP,
            x=x, y=y,
            description=f"Recovery tap #{self.stuck_count} at ({x}, {y})"
        )

    def get_stats(self) -> dict:
        """Return current bot statistics."""
        return {
            "chapter": self.current_chapter,
            "level": self.current_level,
            "levels_completed": self.levels_completed,
            "levels_failed": self.levels_failed,
            "total_stars": self.total_stars,
            "consecutive_fails": self.consecutive_fails,
        }

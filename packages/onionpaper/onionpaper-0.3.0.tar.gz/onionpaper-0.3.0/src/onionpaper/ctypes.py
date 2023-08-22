from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass
from enum import Enum
from string import ascii_lowercase, digits
from typing import Any, Dict, Literal, Optional

import pyautogui
import pytweening


alphanumeric_keys = [*ascii_lowercase, *digits]
mouse_buttons = ["left", "middle", "right"]
duration_range = (0.0, 10.0)

logger = logging.getLogger("onionpaper")
logger.addHandler(logging.StreamHandler())


# noinspection PyProtectedMember, PyUnresolvedReferences
def get_loglevel_value(name: str, fallback: int = 30) -> int:
    return logging._nameToLevel.get(name.upper(), fallback)


def get_tween_func(name: str):
    if hasattr(pytweening, name):
        return getattr(pytweening, name)
    return pytweening.linear


def sanitize_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("\t", "\\t")


def truncate_text(text: str, limit: int) -> str:
    return text[: min(limit, len(text))]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Config:
    loglevel: str = "warning"
    relative: bool = True
    tween: str = "linear"

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Config:
        return Config(**dikt)


class ActionType(StrEnum):
    Click = "click"
    Configure = "configure"
    Drag = "drag"
    Hotkey = "hotkey"
    Move = "move"
    Press = "press"
    Stop = "stop"
    Write = "write"


@dataclass
class Action:
    type: ActionType = ActionType.Move
    x: float = 0.0
    y: float = 0.0
    duration: float = 0.0
    button: str = "left"
    key: str = "return"
    randomize: Optional[str] = None
    text: Optional[str] = None

    loglevel: Optional[str] = None
    relative: Optional[bool] = None
    tween: Optional[str] = None

    def execute(self, config: Config) -> None:
        loglevel = self.loglevel if self.loglevel else config.loglevel
        relative = self.relative if self.relative is not None else config.relative
        tween = self.tween if self.tween else config.tween

        self.randomize_parts(relative=relative)

        self.set_loglevel(loglevel=loglevel)

        if self.type == ActionType.Click:
            self.execute_click()
        if self.type == ActionType.Configure:
            self.execute_configure(config=config)
        elif self.type == ActionType.Drag:
            self.execute_drag(relative=relative, tween=tween)
        elif self.type == ActionType.Move:
            self.execute_move(relative=relative, tween=tween)
        elif self.type == ActionType.Hotkey:
            self.execute_hotkey()
        elif self.type == ActionType.Press:
            self.execute_press()
        elif self.type == ActionType.Stop:
            self.execute_stop()
        elif self.type == ActionType.Write:
            self.execute_write()

    def execute_click(self) -> None:
        pyautogui.mouseDown(button=self.button)
        logger.debug(f"| mouseDown(button={self.button})")
        time.sleep(self.duration)
        pyautogui.mouseUp(button=self.button)
        logger.debug(f"| mouseUp(button={self.button})")
        logger.info("* click")

    def execute_configure(self, config: Config) -> None:
        if self.loglevel:
            config.loglevel = self.loglevel
            logger.debug(f"| loglevel = {self.loglevel}")
        if self.relative is not None:
            config.relative = self.relative
            logger.debug(f"| relative = {self.relative}")
        if self.tween:
            config.tween = self.tween
            logger.debug(f"| tween = {self.tween}")
        logger.info("* configure")

    def execute_drag(self, relative: bool, tween: str) -> None:
        if relative:
            pyautogui.dragRel(
                xOffset=self.x,
                yOffset=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
                button=self.button,
            )
            logger.debug(
                "| dragRel("
                f"xOffset={self.x}, "
                f"yOffset={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween}, "
                f"button={self.button})"
            )
        else:
            pyautogui.dragTo(
                x=self.x,
                y=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
                button=self.button,
            )
            logger.debug(
                "| dragTo("
                f"x={self.x}, "
                f"y={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween}, "
                f"button={self.button})"
            )
        logger.info("* drag")

    def execute_hotkey(self) -> None:
        hotkeys = [hk.strip() for hk in self.key.split("+")]
        interval: float = self.duration / len(hotkeys)
        logger.debug(f"| hotkey({', '.join(hotkeys)}, interval={interval})")
        pyautogui.hotkey(*hotkeys, interval=interval)
        logger.info("* hotkey")

    def execute_move(self, relative: bool, tween: str) -> None:
        if relative:
            pyautogui.moveRel(
                xOffset=self.x,
                yOffset=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
            )
            logger.debug(
                "| moveRel("
                f"xOffset={self.x}, "
                f"yOffset={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween})"
            )
        else:
            pyautogui.moveTo(
                x=self.x,
                y=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
            )
            logger.debug(
                "| moveTo("
                f"x={self.x}, "
                f"y={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween})"
            )
        logger.info("* move")

    def execute_press(self) -> None:
        pyautogui.keyDown(key=self.key)
        logger.debug(f"| keyDown(key={self.key})")
        time.sleep(self.duration)
        pyautogui.keyUp(key=self.key)
        logger.debug(f"| keyUp(key={self.key})")
        logger.info("* press")

    def execute_stop(self) -> None:
        logger.debug(f"| stop()")
        time.sleep(self.duration)
        logger.debug(f"| resume()")
        logger.info("* stop")

    def execute_write(self) -> None:
        interval: float = self.duration / len(self.text)
        logger.debug(
            f"| write('{truncate_text(sanitize_text(self.text), limit=25)}...', interval={interval})"
        )
        pyautogui.write(message=self.text, interval=interval)
        logger.info("* write")

    def randomize_parts(self, relative: bool) -> None:
        if self.randomize:
            randomize_parts = self.randomize.split(",")
            for part in randomize_parts:
                part = part.strip()
                if part == "x":
                    self.x = self.random_coord("x", relative=relative)
                    logger.debug(f"| x = random(<{self.x}>)")
                elif part == "y":
                    self.y = self.random_coord("y", relative=relative)
                    logger.debug(f"| y = random(<{self.y}>)")
                elif part == "duration":
                    self.duration = random.uniform(*duration_range)
                    logger.debug(f"| duration = random(<{self.duration}>)")
                elif part == "button":
                    self.button = random.choice(mouse_buttons)
                    logger.debug(f"| button = random(<{self.button}>)")
                elif part == "key":
                    self.key = random.choice(alphanumeric_keys)
                    logger.debug(f"| key = random(<{self.key}>)")

    # noinspection PyMethodMayBeStatic
    def set_loglevel(self, loglevel: str) -> None:
        logger.setLevel(get_loglevel_value(loglevel))

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Action:
        return Action(**dikt)

    # noinspection PyShadowingBuiltins
    @staticmethod
    def random_coord(
        axis: Literal["x", "y"] = "x",
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        range: float = 100.0,
        relative: bool = True,
    ) -> float:
        if relative:
            if minimum is None and maximum is None:
                minimum = -range * 0.5
                maximum = range * 0.5
            if minimum is None:
                minimum = maximum - range
            if maximum is None:
                maximum = minimum + range
            return random.uniform(minimum, maximum)
        else:
            if minimum is None:
                minimum = 0
            if maximum is None:
                size = pyautogui.size()
                maximum = size[0] if axis == "x" else size[1]
            return random.uniform(minimum, maximum)


__all__ = [
    "Action",
    "ActionType",
    "Config",
    "logger",
]

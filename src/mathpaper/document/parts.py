from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class FreeResponse:
    height: str = "1in"


@dataclass
class Parts:
    parts: list[Any]        # list[Part]
    layout: Any = None      # PartsGrid or None
    labels: str = "alpha"   # "alpha" | "roman" | "numeric"
    indent: bool = True     # add left padding when rendered inside a parent Part


@dataclass
class Part:
    prompt: Any
    body: Any = None            # FreeResponse | Parts; built in __post_init__ if None
    answer: Any | None = None
    answer_space: str | None = None  # backwards-compat shorthand → FreeResponse(height)

    def __post_init__(self):
        if self.body is None:
            self.body = FreeResponse(self.answer_space or "1in")

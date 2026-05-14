from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Part:
    prompt: Any
    answer: Any | None = None
    answer_space: str | None = None

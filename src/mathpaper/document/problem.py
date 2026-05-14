from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Problem:
    prompt: Any
    answer: Any | None = None
    answer_space: str | None = None
    points: int | None = None


@dataclass
class MultipartProblem:
    prompt: Any
    parts: list[Any] = field(default_factory=list)
    figure: Any | None = None
    figure_layout: Any | None = None
    layout: Any | None = None
    points: int | None = None

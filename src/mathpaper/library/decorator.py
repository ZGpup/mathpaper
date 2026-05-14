"""@problem decorator and ProblemDef dataclass."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ProblemDef:
    id: str
    tags: list[str]
    topic: str
    description: str
    difficulty: str = "medium"
    course: str = ""
    _fn: Callable[..., Any] = field(default=None, init=False, repr=False)

    def build(self, **kwargs) -> Any:
        if self._fn is None:
            raise RuntimeError(f"ProblemDef '{self.id}' has no builder attached")
        return self._fn(**kwargs)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tags": self.tags,
            "topic": self.topic,
            "description": self.description,
            "difficulty": self.difficulty,
            "course": self.course,
        }


def problem(
    id: str,
    tags: list[str],
    topic: str,
    description: str,
    difficulty: str = "medium",
    course: str = "",
) -> Callable:
    """Decorate a function to register it as a reusable problem in the library."""
    def decorator(fn: Callable) -> Callable:
        defn = ProblemDef(
            id=id,
            tags=tags,
            topic=topic,
            description=description,
            difficulty=difficulty,
            course=course,
        )
        defn._fn = fn

        module = sys.modules.get(fn.__module__)
        if module is not None:
            if not hasattr(module, "_PROBLEMS"):
                module._PROBLEMS = []
            module._PROBLEMS.append(defn)

        fn._problem_def = defn
        return fn

    return decorator

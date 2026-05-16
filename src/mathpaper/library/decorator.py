"""@problem decorator and ProblemDef dataclass."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from mathpaper.document.templated import TemplatedProblem


@dataclass
class ProblemDef:
    id: str
    tags: list[str]
    topic: str
    description: str
    difficulty: str = "medium"
    course: str = ""
    template_path: Path | None = None  # sibling {id}.typ resolved at decoration time
    _fn: Callable[..., Any] = field(default=None, init=False, repr=False)

    def build(self, **kwargs) -> TemplatedProblem:
        if self._fn is None:
            raise RuntimeError(f"ProblemDef '{self.id}' has no builder attached")
        result = self._fn(**kwargs)

        if not isinstance(result, TemplatedProblem):
            raise TypeError(
                f"Problem '{self.id}' must return a TemplatedProblem, "
                f"got {type(result).__name__}"
            )

        # Late template resolution: fill in the sibling .typ resolved at
        # decoration time, unless the function returned an explicit template.
        if result.template is None:
            if self.template_path is None:
                raise FileNotFoundError(
                    f"Problem '{self.id}' returned a TemplatedProblem but no "
                    f"sibling .typ file was found alongside its .py."
                )
            result.template = self.template_path
        return result

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
    """Decorate a function to register it as a reusable problem in the library.

    The decorated function must return a ``TemplatedProblem`` whose layout
    lives in a sibling ``{id}.typ`` next to the decorating .py file. The
    sibling template is resolved at decoration time.
    """
    def decorator(fn: Callable) -> Callable:
        template_path = _resolve_sibling_typ(fn, id)

        defn = ProblemDef(
            id=id,
            tags=tags,
            topic=topic,
            description=description,
            difficulty=difficulty,
            course=course,
            template_path=template_path,
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


def _resolve_sibling_typ(fn: Callable, problem_id: str) -> Path | None:
    """Find {problem_id}.typ next to the file that defines ``fn``.

    Returns None if the function isn't backed by a file on disk (e.g. defined
    in a REPL or in a string-loaded module) — in that case the user must pass
    an explicit ``template=`` when constructing TemplatedProblem.
    """
    src = getattr(fn, "__code__", None)
    if src is None:
        return None
    py_file = getattr(src, "co_filename", "")
    if not py_file or py_file.startswith("<"):
        return None
    candidate = Path(py_file).parent / f"{problem_id}.typ"
    return candidate if candidate.exists() else None

"""One-line description of this problem."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem

# Uncomment to use a Manim figure:
# from mathpaper.figures.manim import ManimFigure
# from manim import Scene, ...


@problem(
    id="problem_id_001",          # must match this filename and the sibling .typ
    tags=["subject", "topic"],
    topic="Topic Name",
    description="One-line description of what the student does",
    difficulty="medium",          # easy | medium | hard
    course="Course Name",
)
def problem_id_001(seed=None) -> TemplatedProblem:
    return TemplatedProblem(
        points=10,
        context={
            "answers": {
                "part_a": "x",
            },
        },
    )

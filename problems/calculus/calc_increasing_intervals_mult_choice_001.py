"""One-line description of this problem."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem

# Uncomment to use a Manim figure:
# from mathpaper.figures.manim import ManimFigure
# from manim import Scene, ...


@problem(
    id="calc_increasing_intervals_mult_choice_001",
    tags=["subject", "topic"],
    topic="Topic Name",
    description="One-line description of what the student does",
    difficulty="medium",          # easy | medium | hard
    course="Course Name",
)
def calc_increasing_intervals_mult_choice_001(seed=None, points=10) -> TemplatedProblem:
    return TemplatedProblem(
        points=points,
        context={
            "answers": {
                "part_a": "answer as a Typst math string",
                "part_b": "answer as a Typst math string",
            },
        },
    )

"""Algebra: solve a basic two-step linear equation."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem


@problem(
    id="alg_linear_solve_001",
    tags=["algebra", "linear-equations", "solve"],
    topic="Linear Equations",
    description="Solve a two-step linear equation: 2x + 5 = 13",
    difficulty="easy",
    course="Algebra",
)
def alg_linear_solve_001(seed=None) -> TemplatedProblem:
    return TemplatedProblem(
        points=3,
        context={
            "equation": "2x + 5 = 13",
            "answers": {"x": "x = 4"},
        },
    )

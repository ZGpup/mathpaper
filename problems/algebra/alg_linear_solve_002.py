"""Algebra: solve a linear equation requiring distribution."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem


@problem(
    id="alg_linear_solve_002",
    tags=["algebra", "linear-equations", "solve", "distribution"],
    topic="Linear Equations",
    description="Solve a linear equation with distribution: 3(x - 2) = 9",
    difficulty="easy",
    course="Algebra",
)
def alg_linear_solve_002(seed=None) -> TemplatedProblem:
    return TemplatedProblem(
        points=3,
        context={
            "equation": "3(x - 2) = 9",
            "answers": {"x": "x = 5"},
        },
    )

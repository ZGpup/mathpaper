"""Algebra: slope-intercept analysis — slope, y-intercept, graph, and solve."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem


@problem(
    id="alg_linear_analysis_001",
    tags=["algebra", "linear-equations", "slope-intercept", "graphing"],
    topic="Linear Equations",
    description="Identify slope, y-intercept, graph, and solve for x given y = 2x - 1",
    difficulty="easy",
    course="Algebra",
)
def alg_linear_analysis_001(seed=None) -> TemplatedProblem:
    return TemplatedProblem(
        points=8,
        context={
            "equation": "y = 2x - 1",
            "y_target": 7,
            "answers": {
                "slope": "2",
                "y_intercept": "-1",
                "x_solve": "x = 4",
            },
        },
    )

"""Triangle related-rates problem authored via the TemplatedProblem pattern.

The layout lives in `triangle_rate_001.typ` (sibling file). This module
computes the figure and the answer expressions and ships them to the .typ
through context.json.
"""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.figures.geometry import TriangleDiagram
from mathpaper.library import problem


@problem(
    id="triangle_rate_001",
    tags=["calculus", "related-rates", "triangle"],
    topic="Related Rates",
    description="Rate of change of triangle area as the included angle increases",
    difficulty="medium",
    course="Calculus",
)
def triangle_rate_001(seed=None) -> TemplatedProblem:
    fig = TriangleDiagram(
        a=4, b=5,
        a_label=r"a = 4", b_label=r"b = 5",
        theta_label=r"\theta",
        width="100%",
    )
    return TemplatedProblem(
        points=10,
        figures=[fig],
        context={
            "figure": fig.asset_name,
            "answers": {
                "formula_a": "(d A)/(d t) = (3 cos(theta))/5",
                "value_b": '(d A)/(d t) = 3/10 "ft"^2 "/" "s"',
            },
        },
    )

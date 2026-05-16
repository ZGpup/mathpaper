"""Algebra: multipart analysis of a cubic polynomial."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import (
    degree_of,
    end_behavior,
    leading_coefficient,
    max_turning_points,
    polynomial_from_roots,
    positive_intervals,
    real_zeros,
    sympy_to_typst,
    y_intercept,
)


@problem(
    id="alg_cubic_analysis_001",
    tags=["algebra", "cubic", "zeros", "end-behavior", "intervals", "turning-points"],
    topic="Polynomial Analysis",
    description="Multipart analysis of a cubic: zeros, y-intercept, end behavior, positive intervals, turning points",
    difficulty="medium",
    course="Algebra",
)
def alg_cubic_analysis_001(seed=None, roots=None) -> TemplatedProblem:
    if roots is None:
        roots = [-1, 2, 4]
    poly = polynomial_from_roots(roots)
    zeros = real_zeros(poly)
    yint = y_intercept(poly)
    lc = leading_coefficient(poly)
    deg = degree_of(poly)
    end = end_behavior(leading=lc, degree=deg)
    pos = positive_intervals(roots, leading=lc)
    tp = max_turning_points(deg)
    return TemplatedProblem(
        points=10,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(poly)}",
            "answers": {
                "zeros": f"x = {', '.join(str(z) for z in zeros)}",
                "y_intercept": f"(0, {yint})",
                "end_behavior": end,
                "positive_intervals": pos,
                "max_turning_points": str(tp),
            },
        },
    )

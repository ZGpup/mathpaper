"""Algebra: multipart analysis of a quadratic polynomial."""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import (
    degree_of,
    end_behavior,
    leading_coefficient,
    negative_intervals,
    polynomial_from_roots,
    real_zeros,
    sympy_to_typst,
    y_intercept,
)


@problem(
    id="alg_quadratic_analysis_001",
    tags=["algebra", "quadratic", "zeros", "end-behavior", "intervals"],
    topic="Polynomial Analysis",
    description="Multipart analysis of a quadratic: zeros, y-intercept, end behavior, negative intervals",
    difficulty="medium",
    course="Algebra",
)
def alg_quadratic_analysis_001(seed=None, roots=None) -> TemplatedProblem:
    if roots is None:
        roots = [-4, 1]
    poly = polynomial_from_roots(roots)
    zeros = real_zeros(poly)
    yint = y_intercept(poly)
    lc = leading_coefficient(poly)
    deg = degree_of(poly)
    end = end_behavior(leading=lc, degree=deg)
    neg = negative_intervals(roots, leading=lc)
    return TemplatedProblem(
        points=8,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(poly)}",
            "answers": {
                "zeros": f"x = {', '.join(str(z) for z in zeros)}",
                "y_intercept": f"(0, {yint})",
                "end_behavior": end,
                "negative_intervals": neg,
            },
        },
    )

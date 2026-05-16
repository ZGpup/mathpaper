"""Calculus: find f'(x), f''(x), and classify critical points for a degree-4 polynomial."""
from __future__ import annotations

from sympy import symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import critical_points, derivative, second_derivative, sympy_to_typst

x = symbols("x")
_DEFAULT_POLY = x**4 - 8 * x**2 + 7


@problem(
    id="calc_deriv_poly_multipart_001",
    tags=["calculus", "derivatives", "second-derivative", "critical-points", "polynomial"],
    topic="Derivatives",
    description="Find f'(x), f''(x), and classify critical points for a degree-4 polynomial",
    difficulty="medium",
    course="Calculus",
)
def calc_deriv_poly_multipart_001(seed=None) -> TemplatedProblem:
    e = _DEFAULT_POLY
    deriv = derivative(e)
    deriv2 = second_derivative(e)
    crits = critical_points(e)
    crit_str = ", ".join(str(c) for c in crits)
    return TemplatedProblem(
        points=10,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(e)}",
            "answers": {
                "first_deriv": sympy_to_typst(deriv),
                "second_deriv": sympy_to_typst(deriv2),
                "critical_points": f"x = {crit_str}",
            },
        },
    )

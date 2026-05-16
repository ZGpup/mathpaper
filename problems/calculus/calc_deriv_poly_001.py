"""Calculus: find f'(x) for a degree-4 polynomial."""
from __future__ import annotations

from sympy import symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import derivative, sympy_to_typst

x = symbols("x")
_DEFAULT_POLY = x**4 - 8 * x**2 + 7


@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_001(seed=None) -> TemplatedProblem:
    e = _DEFAULT_POLY
    return TemplatedProblem(
        points=4,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(e)}",
            "answers": {
                "derivative": f"f'(x) = {sympy_to_typst(derivative(e))}",
            },
        },
    )

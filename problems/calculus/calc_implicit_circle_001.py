"""Calculus: implicit differentiation of a circle x² + y² = r²."""
from __future__ import annotations

from sympy import Eq, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import implicit_derivative, sympy_to_typst

x, y = symbols("x y")
_DEFAULT_CIRCLE = Eq(x**2 + y**2, 25)


@problem(
    id="calc_implicit_circle_001",
    tags=["calculus", "implicit-differentiation", "circle"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a circle x² + y² = r²",
    difficulty="medium",
    course="Calculus",
)
def calc_implicit_circle_001(seed=None) -> TemplatedProblem:
    c = _DEFAULT_CIRCLE
    dydx = implicit_derivative(c)
    return TemplatedProblem(
        points=6,
        context={
            "equation": sympy_to_typst(c),
            "answers": {
                "dydx": f"(d y)/(d x) = {sympy_to_typst(dydx)}",
            },
        },
    )

"""Calculus: implicit differentiation of a complex mixed-exponent curve."""
from __future__ import annotations

from sympy import Eq, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import implicit_derivative, sympy_to_typst

x, y = symbols("x y")
_DEFAULT_MIXED = Eq(y, x ** (y**x))


@problem(
    id="calc_implicit_mixed_001",
    tags=["calculus", "implicit-differentiation", "exponential"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a complex mixed-exponent curve",
    difficulty="hard",
    course="Calculus",
)
def calc_implicit_mixed_001(seed=None) -> TemplatedProblem:
    c = _DEFAULT_MIXED
    dydx = implicit_derivative(c)
    return TemplatedProblem(
        points=8,
        context={
            "equation": sympy_to_typst(c),
            "answers": {
                "dydx": f"(d y)/(d x) = {sympy_to_typst(dydx)}",
            },
        },
    )

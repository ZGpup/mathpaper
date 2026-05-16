"""Calculus: four-part implicit differentiation drill — polynomial, folium, log, trig."""
from __future__ import annotations

from sympy import Eq, cos, log, sin, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import implicit_derivative, sympy_to_typst

x, y = symbols("x y")


@problem(
    id="calc_implicit_drill_001",
    tags=["calculus", "implicit-differentiation", "logarithmic", "trig"],
    topic="Implicit Differentiation",
    description="Four-part implicit differentiation drill: polynomial, folium, log, trig",
    difficulty="medium",
    course="Calculus",
)
def calc_implicit_drill_001(seed=None) -> TemplatedProblem:
    curves = [
        Eq(x**2 + x * y + y**2, 7),
        Eq(x**3 + y**3, 6 * x * y),
        Eq(log(x * y) + x**2 * y, 4),
        Eq(y * sin(x) + x * cos(y), 1),
    ]
    return TemplatedProblem(
        points=12,
        context={
            "parts": [
                {
                    "equation": sympy_to_typst(c),
                    "answer": f"(d y)/(d x) = {sympy_to_typst(implicit_derivative(c))}",
                }
                for c in curves
            ],
        },
    )

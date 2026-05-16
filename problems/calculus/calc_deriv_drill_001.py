"""Calculus: five-part differentiation drill — log rules, log base-b, arcsin, chain rule, quotient with arccos."""
from __future__ import annotations

from sympy import acos, asin, diff, expand_log, exp, log, sin, sqrt, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import sympy_to_typst

x = symbols("x")


@problem(
    id="calc_deriv_drill_001",
    tags=["calculus", "derivatives", "logarithmic", "chain-rule", "inverse-trig"],
    topic="Derivatives",
    description="Five-part differentiation drill: log rules, log base-b, arcsin, chain rule, quotient with arccos",
    difficulty="medium",
    course="Calculus",
)
def calc_deriv_drill_001(seed=None) -> TemplatedProblem:
    e_a = log((x**2 + 1) / sqrt(3 * x - 2))
    e_b = log(x**3 * sin(x), 5)
    e_c = exp(asin(x))
    e_d_inner = (x**2 + 1) ** 3 * sqrt(x - 4) / (2 * x - 1) ** 5
    e_d = e_d_inner**7
    e_e = (x**3 / 3) / acos(x)

    return TemplatedProblem(
        points=20,
        context={
            "parts": [
                {
                    "expr": sympy_to_typst(e_a),
                    "answer": sympy_to_typst(diff(expand_log(e_a, force=True), x)),
                },
                {
                    "expr": sympy_to_typst(e_b),
                    "answer": sympy_to_typst(diff(e_b, x)),
                },
                {
                    "expr": sympy_to_typst(e_c),
                    "answer": sympy_to_typst(diff(e_c, x)),
                },
                {
                    "expr": f"({sympy_to_typst(e_d_inner)})^7",
                    "answer": sympy_to_typst(diff(e_d, x)),
                },
                {
                    "expr": sympy_to_typst(e_e),
                    "answer": sympy_to_typst(diff(e_e, x)),
                },
            ],
        },
    )

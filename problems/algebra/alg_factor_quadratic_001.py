"""Algebra: factor a quadratic with a leading coefficient completely."""
from __future__ import annotations

from sympy import factor, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import polynomial_from_roots, sympy_to_typst

x = symbols("x")


@problem(
    id="alg_factor_quadratic_001",
    tags=["algebra", "factoring", "quadratic", "leading-coefficient"],
    topic="Factoring",
    description="Factor a quadratic with a leading coefficient completely",
    difficulty="easy",
    course="Algebra",
)
def alg_factor_quadratic_001(seed=None, leading_coeff=2, roots=None) -> TemplatedProblem:
    if roots is None:
        roots = [3, -2]
    poly = leading_coeff * polynomial_from_roots(roots)
    return TemplatedProblem(
        points=4,
        context={
            "polynomial": sympy_to_typst(poly),
            "answers": {
                "factored": sympy_to_typst(factor(poly)),
            },
        },
    )

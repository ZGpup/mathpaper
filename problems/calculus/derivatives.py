"""Calculus: derivatives and implicit differentiation problems."""
from sympy import Eq, symbols

from mathpaper import Math, MultipartProblem, Part, PartsGrid, Problem, Text
from mathpaper.library import problem
from mathpaper.math import sympy_to_typst
from mathpaper.math.calculus import (
    critical_points,
    derivative,
    implicit_derivative,
    second_derivative,
)

x, y = symbols("x y")

_DEFAULT_POLY = x**4 - 8 * x**2 + 7
_DEFAULT_CIRCLE = Eq(x**2 + y**2, 25)
_DEFAULT_MIXED = Eq(y, x ** (y**x))


@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_001(expr=None):
    e = expr if expr is not None else _DEFAULT_POLY
    return Problem(
        prompt=Text(f"Let $f(x) = {sympy_to_typst(e)}$. Find $f'(x)$."),
        answer=Math(f"f'(x) = {sympy_to_typst(derivative(e))}"),
        answer_space="1.2in",
        points=4,
    )


@problem(
    id="calc_deriv_poly_multipart_001",
    tags=["calculus", "derivatives", "second-derivative", "critical-points", "polynomial"],
    topic="Derivatives",
    description="Find f'(x), f''(x), and classify critical points for a degree-4 polynomial",
    difficulty="medium",
    course="Calculus",
)
def calc_deriv_poly_multipart_001(expr=None):
    e = expr if expr is not None else _DEFAULT_POLY
    deriv = derivative(e)
    deriv2 = second_derivative(e)
    crits = critical_points(e)
    crit_str = ", ".join(str(c) for c in crits)
    return MultipartProblem(
        prompt=Text(
            f"Let $f(x) = {sympy_to_typst(e)}$. Answer each question below."
        ),
        parts=[
            Part("Find $f'(x)$.", answer=Math(sympy_to_typst(deriv))),
            Part("Find $f''(x)$.", answer=Math(sympy_to_typst(deriv2))),
            Part(
                "Find all critical points of $f$.",
                answer=Math(f"x = {crit_str}"),
            ),
            Part(
                r"Classify each critical point as a local min, local max, or neither.",
            ),
        ],
        layout=PartsGrid(columns=2, answer_space="1.2in"),
        points=10,
    )


@problem(
    id="calc_implicit_circle_001",
    tags=["calculus", "implicit-differentiation", "circle"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a circle x² + y² = r²",
    difficulty="medium",
    course="Calculus",
)
def calc_implicit_circle_001(curve=None):
    c = curve if curve is not None else _DEFAULT_CIRCLE
    dydx = implicit_derivative(c)
    return Problem(
        prompt=Text(
            f"Given ${sympy_to_typst(c)}$, "
            "use implicit differentiation to find $(d y)/(d x)$."
        ),
        answer=Math(f"(d y)/(d x) = {sympy_to_typst(dydx)}"),
        answer_space="2in",
        points=6,
    )


@problem(
    id="calc_implicit_mixed_001",
    tags=["calculus", "implicit-differentiation", "exponential"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a complex mixed-exponent curve",
    difficulty="hard",
    course="Calculus",
)
def calc_implicit_mixed_001(curve=None):
    c = curve if curve is not None else _DEFAULT_MIXED
    dydx = implicit_derivative(c)
    return Problem(
        prompt=Text(
            f"Given ${sympy_to_typst(c)}$, "
            "use implicit differentiation to find $(d y)/(d x)$."
        ),
        answer=Math(f"(d y)/(d x) = {sympy_to_typst(dydx)}"),
        answer_space="2.5in",
        points=8,
    )

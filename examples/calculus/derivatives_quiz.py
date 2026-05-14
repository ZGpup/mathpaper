"""
Calculus derivatives and implicit differentiation quiz.

Every answer is computed from the expressions defined below.
Change POLY_EXPR, IMPLICIT_CIRCLE_K, or IMPLICIT_ELLIPSE_K and both
the student worksheet and the answer key regenerate — no manual checking.
"""
from sympy import symbols

from mathpaper import Math, MultipartProblem, Part, PartsGrid, Problem, Test, Text
from mathpaper.math import sympy_to_typst
from mathpaper.math.calculus import (
    critical_points,
    derivative,
    implicit_derivative,
    second_derivative,
)

x, y = symbols("x y")

# ── Change these to produce a different quiz ───────────────────────────────
POLY_EXPR         = x**4 - 8*x**2 + 7     # Problems 1 & 2

IMPLICIT_CIRCLE_K = 25                     # Problem 3: x^2 + y^2 = K
IMPLICIT_MIXED_A  = 2                      # Problem 4: Ax^2 + Bxy + y^3 = K
IMPLICIT_MIXED_B  = 1
IMPLICIT_MIXED_K  = 10
# ──────────────────────────────────────────────────────────────────────────


# ---------------------------------------------------------------------------
# Problem 1 — find f'(x) for a polynomial
# ---------------------------------------------------------------------------
p1_deriv = derivative(POLY_EXPR)

p1 = Problem(
    prompt=Text(f"Let $f(x) = {sympy_to_typst(POLY_EXPR)}$.  Find $f'(x)$."),
    answer=Math(f"f'(x) = {sympy_to_typst(p1_deriv)}"),
    answer_space="1.2in",
    points=4,
)


# ---------------------------------------------------------------------------
# Problem 2 — multipart: f'(x), f''(x), critical points
# f(x) = x^4 - 8x^2 + 7 gives f'(x) = 4x^3 - 16x = 4x(x^2 - 4)
# Critical points at x = -2, 0, 2 — all integers, clean to display.
# ---------------------------------------------------------------------------
p2_deriv  = derivative(POLY_EXPR)
p2_deriv2 = second_derivative(POLY_EXPR)
p2_crit   = critical_points(POLY_EXPR)

p2_crit_str = ", ".join(str(c) for c in p2_crit)

p2 = MultipartProblem(
    prompt=Text(
        f"Let $f(x) = {sympy_to_typst(POLY_EXPR)}$. "
        "Answer each question below."
    ),
    parts=[
        Part("Find $f'(x)$.", answer=Math(sympy_to_typst(p2_deriv))),
        Part("Find $f''(x)$.", answer=Math(sympy_to_typst(p2_deriv2))),
        Part(
            "Find all critical points of $f$.",
            answer=Math(f"x = {p2_crit_str}"),
        ),
        Part(
            r"Classify each critical point as a local min, local max, or neither.",
        ),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=10,
)


# ---------------------------------------------------------------------------
# Problem 3 — implicit differentiation of a circle
# x^2 + y^2 = 25  →  dy/dx = -x/y
# ---------------------------------------------------------------------------
F_circle  = x**2 + y**2 - IMPLICIT_CIRCLE_K
p3_dydx   = implicit_derivative(F_circle)

p3 = Problem(
    prompt=Text(
        f"Given $x^2 + y^2 = {IMPLICIT_CIRCLE_K}$, "
        "use implicit differentiation to find $(d y)/(d x)$."
    ),
    answer=Math(f"(d y)/(d x) = {sympy_to_typst(p3_dydx)}"),
    answer_space="2in",
    points=6,
)


# ---------------------------------------------------------------------------
# Problem 4 — implicit differentiation of a mixed-term curve
# 2x^2 + xy + y^3 = 10  →  dy/dx = -(4x + y) / (x + 3y^2)
# ---------------------------------------------------------------------------
F_mixed = (
    IMPLICIT_MIXED_A * x**2
    + IMPLICIT_MIXED_B * x * y
    + y**3
    - IMPLICIT_MIXED_K
)
p4_dydx = implicit_derivative(F_mixed)

p4 = Problem(
    prompt=Text(
        f"Given $2x^2 + x y + y^3 = {IMPLICIT_MIXED_K}$, "
        "use implicit differentiation to find $(d y)/(d x)$."
    ),
    answer=Math(f"(d y)/(d x) = {sympy_to_typst(p4_dydx)}"),
    answer_space="2.5in",
    points=8,
)


# ---------------------------------------------------------------------------
# Assemble and build
# ---------------------------------------------------------------------------
quiz = Test(title="Derivatives Quiz", course="Calculus", version="A")
quiz.add(p1)
quiz.add(p2)
quiz.add(p3)
quiz.add(p4)

quiz.build("out/calculus")
print("Built to out/calculus/")


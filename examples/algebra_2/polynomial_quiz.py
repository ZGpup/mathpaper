"""
Algebra 2 polynomial analysis quiz.

Every answer is computed from the root definitions below.
Change LEADING_COEFF, QUADRATIC_ROOTS, or CUBIC_ROOTS and both
the student worksheet and the answer key regenerate — no manual checking.
"""
from sympy import factor, symbols

from mathpaper import Test, Problem, MultipartProblem, Part, Text, Math, PartsGrid
from mathpaper.math import (
    degree_of,
    end_behavior,
    leading_coefficient,
    max_turning_points,
    negative_intervals,
    polynomial_from_roots,
    positive_intervals,
    real_zeros,
    sympy_to_typst,
    y_intercept,
)

x = symbols("x")

# ── Change these to produce a different quiz ───────────────────────────────
LEADING_COEFF   = 2
QUADRATIC_ROOTS = [3, -2]    # Problem 1: factoring
ANALYSIS_ROOTS  = [-4, 1]    # Problem 2: quadratic analysis
CUBIC_ROOTS     = [-1, 2, 4] # Problem 3: cubic analysis
# ──────────────────────────────────────────────────────────────────────────


# ---------------------------------------------------------------------------
# Problem 1 — factor a quadratic with a leading coefficient
# Demonstrates that factoring generalizes beyond monic polynomials.
# ---------------------------------------------------------------------------
q1_poly     = LEADING_COEFF * polynomial_from_roots(QUADRATIC_ROOTS)
q1_factored = factor(q1_poly)

p1 = Problem(
    prompt=Text(f"Factor completely: ${sympy_to_typst(q1_poly)}$"),
    answer=Math(sympy_to_typst(q1_factored)),
    answer_space="1.2in",
    points=4,
)


# ---------------------------------------------------------------------------
# Problem 2 — multipart analysis of a quadratic
# All answers fall out of ANALYSIS_ROOTS; none are written by hand.
# ---------------------------------------------------------------------------
q2_poly    = polynomial_from_roots(ANALYSIS_ROOTS)
q2_zeros   = real_zeros(q2_poly)
q2_yint    = y_intercept(q2_poly)
q2_lc      = leading_coefficient(q2_poly)
q2_deg     = degree_of(q2_poly)
q2_end     = end_behavior(leading=q2_lc, degree=q2_deg)
q2_neg     = negative_intervals(ANALYSIS_ROOTS, leading=q2_lc)

p2 = MultipartProblem(
    prompt=Text(
        f"Let $f(x) = {sympy_to_typst(q2_poly)}$. "
        "Use algebra to answer the following."
    ),
    parts=[
        Part(
            "Find all real zeros of $f$.",
            answer=Math(", ".join(str(z) for z in q2_zeros)),
        ),
        Part(
            "Find the $y$-intercept.",
            answer=Math(f"(0, {q2_yint})"),
        ),
        Part(
            "Describe the end behavior of $f$.",
            answer=Math(q2_end),
        ),
        Part(
            r"State the interval(s) where $f(x) < 0$.",
            answer=Math(q2_neg),
        ),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=8,
)


# ---------------------------------------------------------------------------
# Problem 3 — multipart analysis of a cubic
# Extends Problem 2 with end behavior direction, positive intervals, and
# turning points — concepts that appear on the cubic but not the quadratic.
# ---------------------------------------------------------------------------
cubic    = polynomial_from_roots(CUBIC_ROOTS)
c_zeros  = real_zeros(cubic)
c_yint   = y_intercept(cubic)
c_lc     = leading_coefficient(cubic)
c_deg    = degree_of(cubic)
c_end    = end_behavior(leading=c_lc, degree=c_deg)
c_pos    = positive_intervals(CUBIC_ROOTS, leading=c_lc)
c_tp     = max_turning_points(c_deg)

p3 = MultipartProblem(
    prompt=Text(
        f"Let $f(x) = {sympy_to_typst(cubic)}$. "
        "Use algebra to answer the following."
    ),
    parts=[
        Part(
            "Find all real zeros of $f$.",
            answer=Math(", ".join(str(z) for z in c_zeros)),
        ),
        Part(
            "Find the $y$-intercept.",
            answer=Math(f"(0, {c_yint})"),
        ),
        Part(
            "Describe the end behavior of $f$.",
            answer=Math(c_end),
        ),
        Part(
            r"State the interval(s) where $f(x) > 0$.",
            answer=Math(c_pos),
        ),
        Part(
            "What is the maximum number of turning points $f$ can have?",
            answer=Math(str(c_tp)),
        ),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=10,
)


# ---------------------------------------------------------------------------
# Assemble and build
# ---------------------------------------------------------------------------
quiz = Test(title="Polynomial Functions Quiz", course="Algebra 2", version="A")
quiz.add(p1)
quiz.add(p2)
quiz.add(p3)

quiz.build("out/algebra_2")
print("Built to out/algebra_2/")

"""
Algebra 2 polynomial analysis quiz.

The core value demo: every answer is computed from the polynomial
definitions below. Change QUADRATIC_ROOTS or CUBIC_ROOTS at the top
and both the student worksheet and the answer key regenerate with
correct answers — no manual checking, no copy/paste errors.
"""
import re
from sympy import symbols, expand, factor, latex

from mathpaper import Test, Problem, MultipartProblem, Part, Text, Math, RawTypst, PartsGrid

x = symbols("x")

# ── Change these to produce a different quiz ───────────────────────────────
QUADRATIC_ROOTS = [1, 2]   # Problem 1 & 2
CUBIC_ROOTS     = [-3, 1, 4]  # Problem 3 (multipart analysis)
# ──────────────────────────────────────────────────────────────────────────


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def tm(expr) -> str:
    """SymPy expression → Typst math string (works for polynomials)."""
    s = latex(expr)
    s = s.replace(r"\left(", "(").replace(r"\right)", ")")
    s = re.sub(r'\^\{(\w)\}', r'^\1', s)        # x^{2}  → x^2
    s = re.sub(r'\^\{([^}]+)\}', r'^(\1)', s)   # x^{10} → x^(10)
    return s


def positive_intervals(roots: list, leading: int = 1) -> str:
    """Typst math string for the intervals where the polynomial is positive."""
    s = sorted(roots)
    test_pts = [s[0] - 1] + [(s[i] + s[i+1]) / 2 for i in range(len(s)-1)] + [s[-1] + 1]
    bounds = ["-oo"] + [str(r) for r in s] + ["+oo"]
    intervals = []
    for i, t in enumerate(test_pts):
        val = leading
        for r in s:
            val *= t - r
        if val > 0:
            intervals.append(f"({bounds[i]}, {bounds[i+1]})")
    return " union ".join(intervals) if intervals else "nothing"


def end_behavior(leading: int, degree: int) -> str:
    """End behavior description as a Typst math string."""
    if leading > 0 and degree % 2 == 1:
        return r'f(x) -> -oo " as " x -> -oo, quad f(x) -> +oo " as " x -> +oo'
    if leading > 0 and degree % 2 == 0:
        return r'f(x) -> +oo " as " x -> plus.minus oo'
    if leading < 0 and degree % 2 == 1:
        return r'f(x) -> +oo " as " x -> -oo, quad f(x) -> -oo " as " x -> +oo'
    return r'f(x) -> -oo " as " x -> plus.minus oo'


# ---------------------------------------------------------------------------
# Problem 1 — factor a quadratic
# The answer is computed: change roots → correct factored form auto-updates.
# ---------------------------------------------------------------------------
q1_poly     = expand((x - QUADRATIC_ROOTS[0]) * (x - QUADRATIC_ROOTS[1]))
q1_factored = factor(q1_poly)

p1 = Problem(
    prompt=Text(f"Factor completely: ${tm(q1_poly)}$"),
    answer=Math(tm(q1_factored)),
    answer_space="1.2in",
    points=4,
)


# ---------------------------------------------------------------------------
# Problem 2 — find the zeros of the same quadratic
# Same roots, different question type — reuses the same source of truth.
# ---------------------------------------------------------------------------
q2_zeros_str = ", ".join(str(r) for r in sorted(QUADRATIC_ROOTS))

p2 = Problem(
    prompt=Text(f"Find all real zeros of $f(x) = {tm(q1_poly)}$."),
    answer=Math(q2_zeros_str),
    answer_space="1in",
    points=3,
)


# ---------------------------------------------------------------------------
# Problem 3 — multipart analysis of a cubic
# All four part-answers fall out of the polynomial definition; none are
# written by hand.
# ---------------------------------------------------------------------------
cubic      = expand((x - CUBIC_ROOTS[0]) * (x - CUBIC_ROOTS[1]) * (x - CUBIC_ROOTS[2]))
c_yint     = int(cubic.subs(x, 0))
c_zeros    = ", ".join(str(r) for r in sorted(CUBIC_ROOTS))
c_end      = end_behavior(leading=1, degree=3)
c_positive = positive_intervals(CUBIC_ROOTS, leading=1)

p3 = MultipartProblem(
    prompt=Text(
        f"Let $f(x) = {tm(cubic)}$. "
        "Use algebra to answer the following."
    ),
    parts=[
        Part(
            "Find all real zeros of $f$.",
            answer=Math(c_zeros),
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
            "State the interval(s) where $f(x) > 0$.",
            answer=Math(c_positive),
        ),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=8,
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
print(f"  Quadratic roots:  {QUADRATIC_ROOTS}  →  factor: {q1_factored}")
print(f"  Cubic roots:      {CUBIC_ROOTS}  →  y-intercept: {c_yint}")

"""Polynomial utilities."""
from sympy import Poly, expand, solve, symbols

from mathpaper.math.expressions import sympy_to_typst  # noqa: F401 — re-export


def polynomial_from_roots(roots: list, var: str = "x"):
    """Return a SymPy polynomial expanded from a list of roots."""
    x = symbols(var)
    poly = 1
    for r in roots:
        poly *= x - r
    return expand(poly)


def polynomial_from_roots_with_multiplicity(roots: dict, var: str = "x"):
    """Return a SymPy polynomial from a {root: multiplicity} dict.

    Example: {2: 2, -1: 1} → (x - 2)^2 * (x + 1)
    """
    x = symbols(var)
    poly = 1
    for root, mult in roots.items():
        poly *= (x - root) ** mult
    return expand(poly)


def leading_coefficient(poly, var: str = "x"):
    """Return the leading coefficient of a SymPy polynomial."""
    x = symbols(var)
    lc = Poly(poly, x).LC()
    f = float(lc)
    return int(f) if f == int(f) else f


def degree_of(poly, var: str = "x") -> int:
    """Return the degree of a SymPy polynomial."""
    x = symbols(var)
    return int(Poly(poly, x).degree())


def y_intercept(poly, var: str = "x"):
    """Return the y-intercept value f(0) of a SymPy polynomial."""
    x = symbols(var)
    f = float(poly.subs(x, 0))
    return int(f) if f == int(f) else f


def real_zeros(poly, var: str = "x") -> list:
    """Return a sorted list of real zeros of a SymPy polynomial."""
    x = symbols(var)
    zeros = []
    for r in solve(poly, x):
        if r.is_real:
            f = float(r)
            zeros.append(int(f) if f == int(f) else f)
    return sorted(zeros)


def max_turning_points(degree: int) -> int:
    """Return the maximum number of turning points for a degree-n polynomial."""
    return degree - 1


def end_behavior(leading: int, degree: int) -> str:
    """Typst math string describing the end behavior of a polynomial."""
    if leading > 0 and degree % 2 == 1:
        return r'f(x) -> -oo " as " x -> -oo, quad f(x) -> +oo " as " x -> +oo'
    if leading > 0 and degree % 2 == 0:
        return r'f(x) -> +oo " as " x -> plus.minus oo'
    if leading < 0 and degree % 2 == 1:
        return r'f(x) -> +oo " as " x -> -oo, quad f(x) -> -oo " as " x -> +oo'
    return r'f(x) -> -oo " as " x -> plus.minus oo'


def _sign_intervals(roots: list, leading: int, positive: bool) -> str:
    s = sorted(roots)
    test_pts = (
        [s[0] - 1]
        + [(s[i] + s[i + 1]) / 2 for i in range(len(s) - 1)]
        + [s[-1] + 1]
    )
    bounds = ["-oo"] + [str(r) for r in s] + ["+oo"]
    intervals = []
    for i, t in enumerate(test_pts):
        val = leading
        for r in s:
            val *= t - r
        if (val > 0) == positive:
            intervals.append(f"({bounds[i]}, {bounds[i + 1]})")
    return " union ".join(intervals) if intervals else "nothing"


def positive_intervals(roots: list, leading: int = 1) -> str:
    """Typst math string for the intervals where the polynomial is positive."""
    return _sign_intervals(roots, leading, positive=True)


def negative_intervals(roots: list, leading: int = 1) -> str:
    """Typst math string for the intervals where the polynomial is negative."""
    return _sign_intervals(roots, leading, positive=False)

"""Calculus utilities — derivatives and implicit differentiation."""
from sympy import diff, simplify, solve, symbols


def derivative(expr, var: str = "x"):
    """Return the first derivative of expr with respect to var."""
    x = symbols(var)
    return diff(expr, x)


def second_derivative(expr, var: str = "x"):
    """Return the second derivative of expr with respect to var."""
    x = symbols(var)
    return diff(expr, x, 2)


def nth_derivative(expr, n: int, var: str = "x"):
    """Return the nth derivative of expr with respect to var."""
    x = symbols(var)
    return diff(expr, x, n)


def implicit_derivative(curve, x_var: str = "x", y_var: str = "y"):
    """Return dy/dx for an implicitly defined curve via implicit differentiation.

    Accepts either:
    - a SymPy Eq, e.g. Eq(x**2 + y**2, 25)  ← preferred; use with sympy_to_typst
    - an expression F equal to zero, e.g. x**2 + y**2 - 25

    Returns a simplified SymPy expression in terms of x and y.
    """
    from sympy import Eq
    x = symbols(x_var)
    y = symbols(y_var)
    F = curve.lhs - curve.rhs if isinstance(curve, Eq) else curve
    return simplify(-diff(F, x) / diff(F, y))


def critical_points(expr, var: str = "x") -> list:
    """Return a sorted list of real critical points (where f' = 0).

    Returns int or float values, matching the convention in real_zeros().
    Non-real or irrational critical points are excluded; use SymPy directly
    for those cases.
    """
    x = symbols(var)
    deriv = diff(expr, x)
    result = []
    for r in solve(deriv, x):
        if r.is_real:
            f = float(r)
            result.append(int(f) if f == int(f) else f)
    return sorted(result)


def tangent_line_at(expr, x0, var: str = "x"):
    """Return (slope, y_intercept) of the tangent line to expr at x = x0.

    Both values are SymPy expressions.
    """
    x = symbols(var)
    slope = diff(expr, x).subs(x, x0)
    y0 = expr.subs(x, x0)
    b = y0 - slope * x0
    return slope, b


def inflection_points(expr, var: str = "x") -> list:
    """Return real x-values where f'' changes sign (true inflection points).

    Returns int or float values, consistent with critical_points().
    """
    x = symbols(var)
    f2 = diff(expr, x, 2)
    result = []
    for r in solve(f2, x):
        if not r.is_real:
            continue
        rv = float(r)
        left = float(f2.subs(x, rv - 1e-4))
        right = float(f2.subs(x, rv + 1e-4))
        if (left > 0) != (right > 0):
            result.append(int(rv) if rv == int(rv) else rv)
    return sorted(result)


def concavity_intervals(expr, var: str = "x") -> dict:
    """Return concavity intervals as Typst-formatted strings.

    Returns {"concave_up": "...", "concave_down": "..."} where each value
    is a Typst math string listing the intervals (e.g. "(-oo, -1) union (1, oo)").
    """
    x = symbols(var)
    f2 = diff(expr, x, 2)
    pts = inflection_points(expr, var)
    breakpoints = [float("-inf")] + list(pts) + [float("inf")]
    up, down = [], []
    for i in range(len(breakpoints) - 1):
        a, b = breakpoints[i], breakpoints[i + 1]
        if a == float("-inf"):
            test = b - 1
        elif b == float("inf"):
            test = a + 1
        else:
            test = (a + b) / 2
        val = float(f2.subs(x, test))
        lo = "-oo" if a == float("-inf") else (str(int(a)) if a == int(a) else str(round(a, 6)))
        hi = "oo" if b == float("inf") else (str(int(b)) if b == int(b) else str(round(b, 6)))
        interval = f"({lo}, {hi})"
        (up if val > 0 else down).append(interval)

    def _join(lst: list) -> str:
        return " union ".join(lst) if lst else "nothing"

    return {"concave_up": _join(up), "concave_down": _join(down)}


def monotone_intervals(expr, var: str = "x") -> dict:
    """Return increasing/decreasing intervals as Typst-formatted strings.

    Uses the symbolic critical points of expr to produce exact interval
    boundaries (e.g. sqrt(3) rather than 1.732...).

    Returns {"increasing": "...", "decreasing": "..."}.
    """
    from mathpaper.math.expressions import sympy_to_typst
    from sympy import solve as _solve
    x = symbols(var)
    fp = diff(expr, x)
    crits_sym = sorted(_solve(fp, x, dict=False), key=lambda r: float(r) if r.is_real else 0)
    crits_sym = [c for c in crits_sym if c.is_real]
    cf = [float(c) for c in crits_sym]
    ct = [sympy_to_typst(c) for c in crits_sym]
    inc, dec = [], []
    for i in range(len(cf) + 1):
        a = cf[i - 1] if i > 0 else float("-inf")
        b = cf[i] if i < len(cf) else float("inf")
        test = b - 1 if a == float("-inf") else a + 1 if b == float("inf") else (a + b) / 2
        val = float(fp.subs(x, test))
        lo = "-oo" if i == 0 else ct[i - 1]
        hi = "oo" if i == len(cf) else ct[i]
        (inc if val > 0 else dec).append(f"({lo}, {hi})")

    def _join(lst: list) -> str:
        return " union ".join(lst) if lst else "nothing"

    return {"increasing": _join(inc), "decreasing": _join(dec)}


def classify_critical_points(expr, var: str = "x") -> dict:
    """Return {x_val: classification} for each critical point.

    Classification is 'local min', 'local max', or 'neither' (when f'' = 0).
    Uses the second derivative test.
    """
    x = symbols(var)
    f2 = diff(expr, x, 2)
    result = {}
    for c in critical_points(expr, var):
        val = float(f2.subs(x, c))
        if val > 0:
            result[c] = "local min"
        elif val < 0:
            result[c] = "local max"
        else:
            result[c] = "neither"
    return result


def implicit_tangent_at(curve, x0, y0, x_var: str = "x", y_var: str = "y"):
    """Return (slope, typst_equation) of the tangent to an implicit curve at (x0, y0).

    slope is a SymPy expression; typst_equation is a formatted string
    "y - {y0} = {slope}(x - {x0})" ready for use in Math(...).
    """
    from sympy import Eq, nsimplify
    x = symbols(x_var)
    y = symbols(y_var)
    dydx = implicit_derivative(curve, x_var, y_var)
    slope = dydx.subs([(x, x0), (y, y0)])
    slope = nsimplify(slope, rational=True)
    from mathpaper.math.expressions import sympy_to_typst
    s = sympy_to_typst(slope)
    x0s = sympy_to_typst(nsimplify(x0))
    y0s = sympy_to_typst(nsimplify(y0))
    eq = f"y - {y0s} = {s}(x - {x0s})"
    return slope, eq

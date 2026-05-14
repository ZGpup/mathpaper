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

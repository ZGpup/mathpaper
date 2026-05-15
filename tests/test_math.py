"""Tests for math helpers: polynomials, sympy_to_typst, calculus."""
import sympy
from sympy import Eq, symbols

from mathpaper.math import (
    derivative,
    end_behavior,
    implicit_derivative,
    polynomial_from_roots,
    real_zeros,
    second_derivative,
    sympy_to_typst,
    y_intercept,
)


x = symbols("x")


def test_polynomial_from_roots():
    poly = polynomial_from_roots([1, -2, 3])
    assert poly == sympy.expand((x - 1) * (x + 2) * (x - 3))


def test_real_zeros_returns_sorted_ints():
    poly = polynomial_from_roots([3, -1, 2])
    assert real_zeros(poly) == [-1, 2, 3]


def test_y_intercept_returns_int_when_integer():
    poly = polynomial_from_roots([1, -1])  # x^2 - 1
    assert y_intercept(poly) == -1


def test_end_behavior_positive_odd_degree():
    s = end_behavior(leading=1, degree=3)
    assert "-oo" in s and "+oo" in s


def test_end_behavior_negative_even_degree():
    s = end_behavior(leading=-1, degree=4)
    assert "plus.minus oo" in s


def test_derivative_polynomial():
    assert derivative(x**3) == 3 * x**2


def test_second_derivative_polynomial():
    assert second_derivative(x**4) == 12 * x**2


def test_implicit_derivative_circle():
    y = symbols("y")
    eq = Eq(x**2 + y**2, 25)
    dydx = implicit_derivative(eq)
    # Should simplify to -x/y
    assert sympy.simplify(dydx - (-x / y)) == 0


def test_sympy_to_typst_polynomial_uses_juxtaposition():
    s = sympy_to_typst(2 * x**2 + 3 * x + 1)
    assert "\\cdot" not in s
    assert "\\frac" not in s
    assert "x^2" in s


def test_sympy_to_typst_fraction_uses_paren_slash():
    # \frac must never appear in the output; sympy prefers (x)/(2) over (1)/(2)·x
    s = sympy_to_typst(sympy.Rational(1, 2) * x)
    assert "\\frac" not in s
    assert "/" in s


def test_sympy_to_typst_strips_left_right():
    expr = sympy.sin(x + 1)
    s = sympy_to_typst(expr)
    assert "\\left" not in s and "\\right" not in s
    assert "sin" in s


def test_sympy_to_typst_handles_sqrt():
    s = sympy_to_typst(sympy.sqrt(x + 1))
    assert "sqrt(" in s and "\\sqrt" not in s


def test_sympy_to_typst_greek_letters():
    alpha = symbols("alpha")
    s = sympy_to_typst(2 * alpha)
    assert "\\alpha" not in s
    assert "alpha" in s

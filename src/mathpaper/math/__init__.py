"""Math module for mathpaper."""
from mathpaper.math.calculus import (
    critical_points,
    derivative,
    implicit_derivative,
    nth_derivative,
    second_derivative,
    tangent_line_at,
)
from mathpaper.math.expressions import sympy_to_typst
from mathpaper.math.polynomials import (
    degree_of,
    end_behavior,
    leading_coefficient,
    max_turning_points,
    negative_intervals,
    polynomial_from_roots,
    polynomial_from_roots_with_multiplicity,
    positive_intervals,
    real_zeros,
    y_intercept,
)

__all__ = [
    "sympy_to_typst",
    # calculus
    "derivative",
    "second_derivative",
    "nth_derivative",
    "implicit_derivative",
    "critical_points",
    "tangent_line_at",
    # polynomials
    "polynomial_from_roots",
    "polynomial_from_roots_with_multiplicity",
    "leading_coefficient",
    "degree_of",
    "y_intercept",
    "real_zeros",
    "max_turning_points",
    "end_behavior",
    "positive_intervals",
    "negative_intervals",
]

"""Polynomial analysis problem — no figure, deep recursive parts.

Demonstrates the multi-level part layout (alpha → roman → numeric) using
Typst's native `+` enum, which auto-indents and auto-labels at each depth.
"""
from __future__ import annotations

from mathpaper import TemplatedProblem
from mathpaper.library import problem


@problem(
    id="polynomial_zeros_001",
    tags=["algebra", "polynomial", "zeros"],
    topic="Polynomial Analysis",
    description="Find zeros, intercepts, end behavior, and intervals of positivity",
    difficulty="medium",
    course="Algebra 2",
)
def polynomial_zeros_001(seed=None) -> TemplatedProblem:
    # Polynomial f(x) = (x+3)(x-1)(x-4), expanded.
    return TemplatedProblem(
        points=12,
        context={
            "polynomial": "f(x) = (x+3)(x-1)(x-4)",
            "answers": {
                "zeros": "x = -3, 1, 4",
                "y_intercept": "f(0) = 12",
                "end_behavior_left": "f(x) -> -infinity",
                "end_behavior_right": "f(x) -> +infinity",
                "positive_intervals": "x in (-3, 1) union (4, infinity)",
            },
        },
    )

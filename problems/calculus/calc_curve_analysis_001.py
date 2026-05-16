"""Calculus: increasing/decreasing intervals, concavity, and critical point classification."""
from __future__ import annotations

from sympy import diff, solve, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import (
    classify_critical_points,
    concavity_intervals,
    inflection_points,
    monotone_intervals,
    sympy_to_typst,
)

x = symbols("x")
_POLY = x**4 - 6 * x**2 + 8


@problem(
    id="calc_curve_analysis_001",
    tags=["calculus", "derivatives", "critical-points", "concavity", "monotone-intervals", "inflection-points"],
    topic="Curve Analysis",
    description="Find increasing/decreasing intervals, concavity, and classify critical points for a degree-4 polynomial",
    difficulty="hard",
    course="Calculus",
)
def calc_curve_analysis_001(seed=None) -> TemplatedProblem:
    poly = _POLY
    mono = monotone_intervals(poly)
    conc = concavity_intervals(poly)
    classified = classify_critical_points(poly)

    critical_pts = sorted(solve(diff(poly, x), x), key=float)
    critical_str = ", ".join(f"x = {sympy_to_typst(c)}" for c in critical_pts)
    inflection_str = ", ".join(str(v) for v in inflection_points(poly))
    classification_str = "; ".join(
        f'x = {sympy_to_typst(c)}: "{classified[float(c)]}"'
        for c in critical_pts
    )

    return TemplatedProblem(
        points=12,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(poly)}",
            "answers": {
                "increasing": mono["increasing"],
                "decreasing": mono["decreasing"],
                "critical_points": critical_str,
                "concave_up": conc["concave_up"],
                "concave_down": conc["concave_down"],
                "inflection_points": f"x = {inflection_str}",
                "classifications": classification_str,
            },
        },
    )

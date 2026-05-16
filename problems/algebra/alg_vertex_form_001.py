"""Algebra: vertex-form quadratic — transformations, key features, range."""
from __future__ import annotations

from sympy import Rational, sqrt, symbols

from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import sympy_to_typst

x = symbols("x")


@problem(
    id="alg_vertex_form_001",
    tags=["algebra", "quadratic", "vertex-form", "transformations", "key-features"],
    topic="Vertex Form",
    description="Vertex-form quadratic: describe transformations and find key features with nested sub-parts",
    difficulty="medium",
    course="Algebra",
)
def alg_vertex_form_001(seed=None, a=-2, h=3, k=8) -> TemplatedProblem:
    poly = a * (x - h) ** 2 + k
    x_intercepts = [h - sqrt(Rational(-k, a)), h + sqrt(Rational(-k, a))]
    yint = int(poly.subs(x, 0))
    return TemplatedProblem(
        points=12,
        context={
            "polynomial": f"f(x) = {sympy_to_typst(poly)}",
            "a": a,
            "h": h,
            "k": k,
            "h_abs": abs(h),
            "k_abs": abs(k),
            "a_abs": abs(a),
            "a_negative": a < 0,
            "h_positive": h > 0,
            "k_positive": k > 0,
            "answers": {
                "vertex": f"({h}, {k})",
                "axis": f"x = {h}",
                "x_intercepts": f"x = {', '.join(sympy_to_typst(z) for z in x_intercepts)}",
                "y_intercept": f"(0, {yint})",
                "range": f"(-oo, {k}]" if a < 0 else f"[{k}, oo)",
            },
        },
    )

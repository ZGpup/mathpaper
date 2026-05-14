"""Calculus: derivatives and implicit differentiation problems."""
from sympy import Eq, symbols

from mathpaper import Math, MultipartProblem, Part, PartsGrid, Problem, Text
from mathpaper.library import problem
from mathpaper.math import sympy_to_typst
from mathpaper.math.calculus import (
    critical_points,
    derivative,
    implicit_derivative,
    second_derivative,
)

x, y = symbols("x y")

_DEFAULT_POLY = x**4 - 8 * x**2 + 7
_DEFAULT_CIRCLE = Eq(x**2 + y**2, 25)
_DEFAULT_MIXED = Eq(y, x ** (y**x))


@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_001(expr=None):
    e = expr if expr is not None else _DEFAULT_POLY
    return Problem(
        prompt=Text(f"Let $f(x) = {sympy_to_typst(e)}$. Find $f'(x)$."),
        answer=Math(f"f'(x) = {sympy_to_typst(derivative(e))}"),
        answer_space="1.2in",
        points=4,
    )


@problem(
    id="calc_deriv_poly_multipart_001",
    tags=["calculus", "derivatives", "second-derivative", "critical-points", "polynomial"],
    topic="Derivatives",
    description="Find f'(x), f''(x), and classify critical points for a degree-4 polynomial",
    difficulty="medium",
    course="Calculus",
)
def calc_deriv_poly_multipart_001(expr=None):
    e = expr if expr is not None else _DEFAULT_POLY
    deriv = derivative(e)
    deriv2 = second_derivative(e)
    crits = critical_points(e)
    crit_str = ", ".join(str(c) for c in crits)
    return MultipartProblem(
        prompt=Text(
            f"Let $f(x) = {sympy_to_typst(e)}$. Answer each question below."
        ),
        parts=[
            Part("Find $f'(x)$.", answer=Math(sympy_to_typst(deriv))),
            Part("Find $f''(x)$.", answer=Math(sympy_to_typst(deriv2))),
            Part(
                "Find all critical points of $f$.",
                answer=Math(f"x = {crit_str}"),
            ),
            Part(
                r"Classify each critical point as a local min, local max, or neither.",
            ),
        ],
        layout=PartsGrid(columns=2, answer_space="1.2in"),
        points=10,
    )


@problem(
    id="calc_implicit_circle_001",
    tags=["calculus", "implicit-differentiation", "circle"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a circle x² + y² = r²",
    difficulty="medium",
    course="Calculus",
)
def calc_implicit_circle_001(curve=None):
    c = curve if curve is not None else _DEFAULT_CIRCLE
    dydx = implicit_derivative(c)
    return Problem(
        prompt=Text(
            f"Given ${sympy_to_typst(c)}$, "
            "use implicit differentiation to find $(d y)/(d x)$."
        ),
        answer=Math(f"(d y)/(d x) = {sympy_to_typst(dydx)}"),
        answer_space="2in",
        points=6,
    )


@problem(
    id="calc_implicit_mixed_001",
    tags=["calculus", "implicit-differentiation", "exponential"],
    topic="Implicit Differentiation",
    description="Implicit differentiation of a complex mixed-exponent curve",
    difficulty="hard",
    course="Calculus",
)
def calc_implicit_mixed_001(curve=None):
    c = curve if curve is not None else _DEFAULT_MIXED
    dydx = implicit_derivative(c)
    return Problem(
        prompt=Text(
            f"Given ${sympy_to_typst(c)}$, "
            "use implicit differentiation to find $(d y)/(d x)$."
        ),
        answer=Math(f"(d y)/(d x) = {sympy_to_typst(dydx)}"),
        answer_space="2.5in",
        points=8,
    )


@problem(
    id="calc_deriv_drill_001",
    tags=["calculus", "derivatives", "logarithmic", "chain-rule", "inverse-trig"],
    topic="Derivatives",
    description="Five-part differentiation drill: log rules, log base-b, arcsin, chain rule, quotient with arccos",
    difficulty="medium",
    course="Calculus",
)
def calc_deriv_drill_001():
    from sympy import acos, asin, diff, expand_log, exp, log, sin, sqrt, symbols
    from mathpaper import Math, MultipartProblem, Part, PartsGrid, Text
    from mathpaper.math import sympy_to_typst

    x = symbols("x")

    e3a = log((x**2 + 1) / sqrt(3*x - 2))
    e3b_arg = x**3 * sin(x)
    e3c = exp(asin(x))
    e3d_inner = (x**2 + 1)**3 * sqrt(x - 4) / (2*x - 1)**5
    e3e = (x**3 / 3) / acos(x)

    return MultipartProblem(
        prompt=Text(
            "Differentiate each of the following. "
            "These derivative rules were derived using implicit differentiation. "
            "You do not need to simplify your answers."
        ),
        parts=[
            Part(
                f"$y = {sympy_to_typst(e3a)}$. Find $y'$.",
                answer=Math(sympy_to_typst(diff(expand_log(e3a, force=True), x))),
            ),
            Part(
                f"$y = {sympy_to_typst(log(e3b_arg, 5))}$. Find $y'$.",
                answer=Math(sympy_to_typst(diff(log(e3b_arg, 5), x))),
            ),
            Part(
                f"$y = {sympy_to_typst(e3c)}$. Find $y'$.",
                answer=Math(sympy_to_typst(diff(e3c, x))),
            ),
            Part(
                f"$y = ({sympy_to_typst(e3d_inner)})^7$. Find $y'$.",
                answer=Math(
                    f"7 ({sympy_to_typst(e3d_inner)})^7 "
                    r"((6 x)/(x^2+1) + 1/(2(x-4)) - 10/(2x-1))"
                ),
            ),
            Part(
                f"$y = {sympy_to_typst(e3e)}$. Find $y'$.",
                answer=Math(sympy_to_typst(diff(e3e, x))),
            ),
        ],
        layout=PartsGrid(columns=2, answer_space="1.8in"),
        points=20,
    )


@problem(
    id="calc_implicit_drill_001",
    tags=["calculus", "implicit-differentiation", "logarithmic", "trig"],
    topic="Implicit Differentiation",
    description="Four-part implicit differentiation drill: polynomial, folium, log, trig",
    difficulty="medium",
    course="Calculus",
)
def calc_implicit_drill_001():
    from sympy import Eq, cos, log, sin, symbols
    from mathpaper import Math, MultipartProblem, Part, PartsGrid, Text
    from mathpaper.math import implicit_derivative, sympy_to_typst

    x, y = symbols("x y")

    c4a = Eq(x**2 + x*y + y**2, 7)
    c4b = Eq(x**3 + y**3, 6*x*y)
    c4c = Eq(log(x*y) + x**2*y, 4)
    c4d = Eq(y*sin(x) + x*cos(y), 1)

    return MultipartProblem(
        prompt=Text(r"For each implicit curve below, find $(d y)/(d x)$."),
        parts=[
            Part(
                f"${sympy_to_typst(c4a)}$",
                answer=Math(sympy_to_typst(implicit_derivative(c4a))),
            ),
            Part(
                f"${sympy_to_typst(c4b)}$",
                answer=Math(sympy_to_typst(implicit_derivative(c4b))),
            ),
            Part(
                f"${sympy_to_typst(c4c)}$",
                answer=Math(sympy_to_typst(implicit_derivative(c4c))),
            ),
            Part(
                f"${sympy_to_typst(c4d)}$",
                answer=Math(sympy_to_typst(implicit_derivative(c4d))),
            ),
        ],
        layout=PartsGrid(columns=2, answer_space="2in"),
        points=12,
    )


@problem(
    id="calc_curve_analysis_001",
    tags=["calculus", "derivatives", "critical-points", "concavity", "monotone-intervals", "inflection-points"],
    topic="Curve Analysis",
    description="Find increasing/decreasing intervals, concavity, and classify critical points for a degree-4 polynomial",
    difficulty="hard",
    course="Calculus",
)
def calc_curve_analysis_001():
    from sympy import diff, solve, symbols
    from mathpaper import Math, MultipartProblem, Part, PartsGrid, Text
    from mathpaper.math import (
        classify_critical_points,
        concavity_intervals,
        inflection_points,
        monotone_intervals,
        sympy_to_typst,
    )

    x = symbols("x")
    poly = x**4 - 6*x**2 + 8

    mono       = monotone_intervals(poly)
    conc       = concavity_intervals(poly)
    classified = classify_critical_points(poly)

    critical_pts   = sorted(solve(diff(poly, x), x), key=float)
    critical_str   = ", ".join(sympy_to_typst(c) for c in critical_pts)
    inflection_str = ", ".join(str(v) for v in inflection_points(poly))
    classification_str = "; ".join(
        f"$x = {sympy_to_typst(cs)}$: {classified[cf]}"
        for cs, cf in zip(critical_pts, sorted(classified))
    )

    return MultipartProblem(
        prompt=Text(f"Given the function $f(x) = {sympy_to_typst(poly)}$, answer the following."),
        parts=[
            Part(
                "Find the intervals on which $f$ is increasing and decreasing. "
                "Identify the $x$-values of any critical points.",
                answer=Math(
                    f"\"Increasing: \" {mono['increasing']}; "
                    f"\"Decreasing: \" {mono['decreasing']}; "
                    f"\"Critical pts: \" x = {critical_str}"
                ),
            ),
            Part(
                "Find the intervals on which $f$ is concave up and concave down. "
                "Identify the $x$-values of any inflection points.",
                answer=Math(
                    f"\"Concave up: \" {conc['concave_up']}; "
                    f"\"Concave down: \" {conc['concave_down']}; "
                    f"\"Inflection pts: \" x = {inflection_str}"
                ),
            ),
            Part(
                "Which of the critical points are local maxima, local minima, or neither?",
                answer=Text(classification_str),
            ),
        ],
        layout=PartsGrid(columns=1, answer_space="1.5in"),
        points=12,
    )

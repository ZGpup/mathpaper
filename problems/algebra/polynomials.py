"""Algebra: polynomial analysis problems."""
from sympy import expand, factor, sqrt, Rational, symbols

from mathpaper import Math, MultipartProblem, Part, Parts, PartsGrid, Problem, Text
from mathpaper.library import problem
from mathpaper.math import (
    degree_of,
    end_behavior,
    leading_coefficient,
    max_turning_points,
    negative_intervals,
    polynomial_from_roots,
    positive_intervals,
    real_zeros,
    sympy_to_typst,
    y_intercept,
)

x = symbols("x")


@problem(
    id="alg_factor_quadratic_001",
    tags=["algebra", "factoring", "quadratic", "leading-coefficient"],
    topic="Factoring",
    description="Factor a quadratic with a leading coefficient completely",
    difficulty="easy",
    course="Algebra",
)
def alg_factor_quadratic_001(leading_coeff=2, roots=None):
    roots = roots if roots is not None else [3, -2]
    poly = leading_coeff * polynomial_from_roots(roots)
    return Problem(
        prompt=Text(f"Factor completely: ${sympy_to_typst(poly)}$"),
        answer=Math(sympy_to_typst(factor(poly))),
        answer_space="1.2in",
        points=4,
    )


@problem(
    id="alg_quadratic_analysis_001",
    tags=["algebra", "quadratic", "zeros", "end-behavior", "intervals"],
    topic="Polynomial Analysis",
    description="Multipart analysis of a quadratic: zeros, y-intercept, end behavior, negative intervals",
    difficulty="medium",
    course="Algebra",
)
def alg_quadratic_analysis_001(roots=None):
    roots = roots if roots is not None else [-4, 1]
    poly = polynomial_from_roots(roots)
    zeros = real_zeros(poly)
    yint = y_intercept(poly)
    lc = leading_coefficient(poly)
    deg = degree_of(poly)
    end = end_behavior(leading=lc, degree=deg)
    neg = negative_intervals(roots, leading=lc)
    return MultipartProblem(
        prompt=Text(
            f"Let $f(x) = {sympy_to_typst(poly)}$. "
            "Use algebra to answer the following."
        ),
        parts=[
            Part("Find all real zeros of $f$.", answer=Math(", ".join(str(z) for z in zeros))),
            Part("Find the $y$-intercept.", answer=Math(f"(0, {yint})")),
            Part("Describe the end behavior of $f$.", answer=Math(end)),
            Part(r"State the interval(s) where $f(x) < 0$.", answer=Math(neg)),
        ],
        layout=PartsGrid(columns=2, answer_space="1.2in"),
        points=8,
    )


@problem(
    id="alg_cubic_analysis_001",
    tags=["algebra", "cubic", "zeros", "end-behavior", "intervals", "turning-points"],
    topic="Polynomial Analysis",
    description="Multipart analysis of a cubic: zeros, y-intercept, end behavior, positive intervals, turning points",
    difficulty="medium",
    course="Algebra",
)
def alg_cubic_analysis_001(roots=None):
    roots = roots if roots is not None else [-1, 2, 4]
    poly = polynomial_from_roots(roots)
    zeros = real_zeros(poly)
    yint = y_intercept(poly)
    lc = leading_coefficient(poly)
    deg = degree_of(poly)
    end = end_behavior(leading=lc, degree=deg)
    pos = positive_intervals(roots, leading=lc)
    tp = max_turning_points(deg)
    return MultipartProblem(
        prompt=Text(
            f"Let $f(x) = {sympy_to_typst(poly)}$. "
            "Use algebra to answer the following."
        ),
        parts=[
            Part("Find all real zeros of $f$.", answer=Math(", ".join(str(z) for z in zeros))),
            Part("Find the $y$-intercept.", answer=Math(f"(0, {yint})")),
            Part("Describe the end behavior of $f$.", answer=Math(end)),
            Part(r"State the interval(s) where $f(x) > 0$.", answer=Math(pos)),
            Part(
                "What is the maximum number of turning points $f$ can have?",
                answer=Math(str(tp)),
            ),
        ],
        layout=PartsGrid(columns=2, answer_space="1.2in"),
        points=10,
    )


@problem(
    id="alg_vertex_form_001",
    tags=["algebra", "quadratic", "vertex-form", "transformations", "key-features"],
    topic="Vertex Form",
    description="Vertex-form quadratic: describe transformations and find key features with nested sub-parts",
    difficulty="medium",
    course="Algebra",
)
def alg_vertex_form_001(a=-2, h=3, k=8):
    poly = a * (x - h)**2 + k
    x_intercepts = [h - sqrt(Rational(-k, a)), h + sqrt(Rational(-k, a))]
    yint = int(poly.subs(x, 0))
    return MultipartProblem(
        prompt=Text(
            f"Let $f(x) = {sympy_to_typst(poly)}$, written in vertex form $a(x-h)^2 + k$."
        ),
        parts=[
            Part(
                prompt=Text(
                    "Describe the three transformations applied to $y = x^2$ to produce $f$."
                ),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=1, answer_space="0.7in"),
                    parts=[
                        Part(
                            f"Horizontal shift: {'right' if h > 0 else 'left'} "
                            f"${abs(h)}$ unit{'s' if abs(h) != 1 else ''}.",
                            answer=Text(
                                f"Replace $x$ with $x - {h}$; shifts the graph right ${h}$."
                            ),
                        ),
                        Part(
                            f"Vertical stretch/reflection by a factor of ${abs(a)}$"
                            + (" with a reflection over the $x$-axis." if a < 0 else "."),
                            answer=Text(
                                f"Multiply output by ${a}$; stretches by ${abs(a)}$ and flips."
                            ),
                        ),
                        Part(
                            f"Vertical shift {'up' if k > 0 else 'down'} ${abs(k)}$ units.",
                            answer=Text(f"Add ${k}$ to the output; shifts the graph up ${k}$."),
                        ),
                    ],
                ),
            ),
            Part(
                prompt=Text(
                    "Find the key features of $f$. "
                    "Note how sub-parts i–iv are arranged in a two-column grid."
                ),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=2, answer_space="0.9in"),
                    parts=[
                        Part("State the vertex.", answer=Math(f"({h}, {k})")),
                        Part("State the axis of symmetry.", answer=Math(f"x = {h}")),
                        Part(
                            "Find the $x$-intercepts algebraically.",
                            answer=Math(
                                "x = " + ", ".join(sympy_to_typst(z) for z in x_intercepts)
                            ),
                        ),
                        Part("Find the $y$-intercept.", answer=Math(f"(0, {yint})")),
                    ],
                ),
            ),
            Part(
                "State the range of $f$ using interval notation.",
                answer=Math(f"(-infinity, {k}]" if a < 0 else f"[{k}, infinity)"),
                answer_space="0.8in",
            ),
        ],
        layout=PartsGrid(columns=1, answer_space="0.8in"),
        points=12,
    )

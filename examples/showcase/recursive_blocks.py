"""Recursive block architecture showcase.

Demonstrates the expressive power of the recursive Block → Parts → Part tree:

  P1  Simple free-response baseline
  P2  Side figure + 2×2 top-level grid  (all FreeResponse leaves)
  P3  Two-level nesting: one part hosts a 2×2 roman inner grid; siblings are flat
  P4  Inner 3-column grid for one part; sibling parts are flat FreeResponse
  P5  Three-level nesting: alpha → roman → numeric  (3 levels deep)
  P6  Outer 3-column grid with heterogeneous cell contents  (flat vs. nested)
  P7  Outer 2-column grid where each cell is itself an inner 2-column grid
  P8  indent=True vs indent=False on sibling parts at the same level
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from mathpaper import (
    Test, Problem, MultipartProblem,
    Parts, Part, FreeResponse, PartsGrid, SideFigure,
    Text, Math, Figure,
)

# ---------------------------------------------------------------------------
# Placeholder figures (generated with Matplotlib; cached in _figures/)
# ---------------------------------------------------------------------------

FIGURES_DIR = Path(__file__).parent / "_figures"
FIGURES_DIR.mkdir(exist_ok=True)


def _make_cubic() -> Path:
    """g(x) = (x+3)(x-1)(x-4) — three labeled real zeros."""
    path = FIGURES_DIR / "graph_cubic.png"
    x = np.linspace(-4.5, 5.5, 600)
    y = (x + 3) * (x - 1) * (x - 4)
    fig, ax = plt.subplots(figsize=(3.5, 3))
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.plot(x, y, "#1f77b4", lw=1.5)
    for rx, label in [(-3, "−3"), (1, "1"), (4, "4")]:
        ax.plot(rx, 0, "ko", ms=5)
        ax.annotate(label, (rx, 0), textcoords="offset points",
                    xytext=(3, 8), fontsize=8)
    ax.set_xlim(-5, 6)
    ax.set_ylim(-32, 28)
    ax.set_title(r"$g(x) = (x+3)(x-1)(x-4)$", fontsize=8)
    ax.grid(True, alpha=0.3, ls="--")
    fig.tight_layout()
    fig.savefig(str(path), dpi=100, bbox_inches="tight")
    plt.close(fig)
    return path


def _make_rational() -> Path:
    """h(x) = 1/(x²−1) — two vertical asymptotes at x = ±1."""
    path = FIGURES_DIR / "graph_rational.png"
    fig, ax = plt.subplots(figsize=(3.5, 3))
    for seg in [
        np.linspace(-4.0, -1.08, 300),
        np.linspace(-0.92,  0.92, 200),
        np.linspace( 1.08,  4.0, 300),
    ]:
        with np.errstate(divide="ignore", invalid="ignore"):
            y = 1.0 / (seg ** 2 - 1)
        y[np.abs(y) > 6] = np.nan
        ax.plot(seg, y, "#d62728", lw=1.5)
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.axvline(-1, color="gray", lw=0.8, ls="--", alpha=0.7)
    ax.axvline( 1, color="gray", lw=0.8, ls="--", alpha=0.7)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-5, 5)
    ax.set_title(r"$h(x) = 1/(x^2-1)$", fontsize=8)
    ax.grid(True, alpha=0.3, ls="--")
    fig.tight_layout()
    fig.savefig(str(path), dpi=100, bbox_inches="tight")
    plt.close(fig)
    return path


cubic_path    = _make_cubic()
rational_path = _make_rational()

fig_cubic    = Figure(cubic_path,    width="100%")
fig_rational = Figure(rational_path, width="100%")

# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

exam = Test(
    title="Recursive Block Architecture — Showcase",
    course="Mathematics",
    version="Demo",
)

# ===========================================================================
# P1  Simple free-response  (baseline: Block → FreeResponse)
# ===========================================================================
exam.add(Problem(
    prompt=Text("Factor completely over the integers: $6x^2 - 7x - 3$."),
    answer=Math("(3x + 1)(2x - 3)"),
    answer_space="1in",
    points=3,
))

# ===========================================================================
# P2  Side figure + 2×2 top-level grid
#     All four parts are FreeResponse leaves.  The figure sits in a side
#     column to the right.  Demonstrates that PartsGrid and SideFigure
#     compose without collision.
#
#     Tree: Block → Parts(PartsGrid(2)) + Figure(SideFigure)
#               ├── Part → FreeResponse
#               ├── Part → FreeResponse
#               ├── Part → FreeResponse
#               └── Part → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text(
        "The graph of $g(x) = (x+3)(x-1)(x-4)$ is shown. "
        "Use it to answer each question."
    ),
    figure=fig_cubic,
    figure_layout=SideFigure(position="right", width="42%"),
    parts=Parts(
        labels="alpha",
        layout=PartsGrid(columns=2, answer_space="0.75in"),
        parts=[
            Part(prompt=Text("State all real zeros of $g$."),
                 answer=Math("-3, 1, 4")),
            Part(prompt=Text("Find the $y$-intercept."),
                 answer=Math("(0, 12)")),
            Part(prompt=Text("Describe the end behavior as $x -> +infinity$."),
                 answer=Math("g(x) -> +infinity")),
            Part(prompt=Text("On what interval(s) is $g(x) > 0$?"),
                 answer=Math("(-3, 1) union (4, +infinity)")),
        ],
    ),
    points=8,
))

# ===========================================================================
# P3  Two-level nesting: alpha outer list, roman inner grid for part (a)
#     Part (a) hosts a 2×2 roman sub-grid; parts (b) and (c) are flat siblings.
#     Mixing a nested-Parts child with FreeResponse siblings at the same level
#     is handled uniformly — the renderer dispatches on body type per part.
#
#     Tree: Block → Parts(no grid)
#               ├── Part (a) → Parts(PartsGrid(2), roman)
#               │                  ├── Part → FreeResponse
#               │                  ├── Part → FreeResponse
#               │                  ├── Part → FreeResponse
#               │                  └── Part → FreeResponse
#               ├── Part (b) → FreeResponse
#               └── Part (c) → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text(
        "Let $h(x) = 1/(x^2 - 1)$. The graph is shown at right."
    ),
    figure=fig_rational,
    figure_layout=SideFigure(position="right", width="40%"),
    parts=Parts(
        labels="alpha",
        parts=[
            Part(
                prompt=Text(
                    "Evaluate each one-sided limit. "
                    "Then state all vertical asymptotes."
                ),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=2, answer_space="0.7in"),
                    parts=[
                        Part(prompt=Math("lim_(x -> -1^-) h(x) ="),
                             answer=Math("+infinity")),
                        Part(prompt=Math("lim_(x -> -1^+) h(x) ="),
                             answer=Math("-infinity")),
                        Part(prompt=Math("lim_(x -> 1^-) h(x) ="),
                             answer=Math("-infinity")),
                        Part(prompt=Math("lim_(x -> 1^+) h(x) ="),
                             answer=Math("+infinity")),
                    ],
                ),
            ),
            Part(
                prompt=Text(
                    "Find the horizontal asymptote of $h$. "
                    "Justify using a limit as $x -> +infinity$."
                ),
                answer=Math("y = 0"),
                answer_space="0.8in",
            ),
            Part(
                prompt=Text("On what interval(s) is $h(x) > 0$?"),
                answer=Math("(-infinity, -1) union (1, +infinity)"),
                answer_space="0.8in",
            ),
        ],
    ),
    points=10,
))

# ===========================================================================
# P4  Inner 3-column grid for one part; siblings are flat FreeResponse
#     The outer list has no grid.  Only part (b) fans out into a 3-column
#     inner grid of six roman sub-parts.  Parts (a) and (c) sit beside it as
#     ordinary free-response items — impossible to express cleanly in LaTeX
#     without nested minipage or tabular hacks.
#
#     Tree: Block → Parts(no grid)
#               ├── Part (a) → FreeResponse
#               ├── Part (b) → Parts(PartsGrid(3), roman)   ← only this fans out
#               │                  ├── Part i   → FreeResponse
#               │                  ├── Part ii  → FreeResponse
#               │                  ├── Part iii → FreeResponse
#               │                  ├── Part iv  → FreeResponse
#               │                  ├── Part v   → FreeResponse
#               │                  └── Part vi  → FreeResponse
#               └── Part (c) → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text(
        "Evaluate the following definite integrals. "
        "Show substitution steps for part (b)."
    ),
    parts=Parts(
        labels="alpha",
        parts=[
            Part(
                prompt=Text(
                    "State the Fundamental Theorem of Calculus (Evaluation Form): "
                    "if $F'(x) = f(x)$, then $integral_a^b f(x) d x =$"
                ),
                answer=Math("F(b) - F(a)"),
                answer_space="0.65in",
            ),
            Part(
                prompt=Text("Evaluate each integral using the result from (a)."),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=3, answer_space="1in"),
                    parts=[
                        Part(prompt=Math("integral_0^(pi/2) cos x d x"),
                             answer=Math("1")),
                        Part(prompt=Math("integral_1^e 1/x d x"),
                             answer=Math("1")),
                        Part(prompt=Math("integral_0^1 2x e^(x^2) d x"),
                             answer=Math("e - 1")),
                        Part(prompt=Math("integral_0^pi sin x d x"),
                             answer=Math("2")),
                        Part(prompt=Math("integral_1^4 1/(2 sqrt(x)) d x"),
                             answer=Math("1")),
                        Part(prompt=Math("integral_0^(ln 2) e^x d x"),
                             answer=Math("1")),
                    ],
                ),
            ),
            Part(
                prompt=Text(
                    "Four integrals in (b) share the same numerical value. "
                    "List them and explain what this means geometrically."
                ),
                answer_space="0.75in",
            ),
        ],
    ),
    points=12,
))

# ===========================================================================
# P5  Three-level nesting: alpha → roman → numeric  (deepest supported)
#     Roman parts (i) and (ii) each carry a numeric inner grid.  Roman
#     part (iii) is a flat FreeResponse leaf.  The renderer recurses without
#     any special cases — only the label scheme and answer_space change.
#
#     Tree: Block → Parts(alpha)
#               ├── Part (a) → FreeResponse
#               ├── Part (b) → Parts(roman)
#               │                  ├── Part (i)   → Parts(numeric, PartsGrid(3))
#               │                  │                    ├── Part 1 → FreeResponse
#               │                  │                    ├── Part 2 → FreeResponse
#               │                  │                    └── Part 3 → FreeResponse
#               │                  ├── Part (ii)  → Parts(numeric, PartsGrid(2))
#               │                  │                    ├── Part 1 → FreeResponse
#               │                  │                    ├── Part 2 → FreeResponse
#               │                  │                    ├── Part 3 → FreeResponse
#               │                  │                    └── Part 4 → FreeResponse
#               │                  └── Part (iii) → FreeResponse
#               └── Part (c) → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text(
        'Let $f(x) = cases(x^2 - 1 quad "if" x < 0, 2x + 1 quad "if" x >= 0)$. '
        "Analyze the continuity of $f$."
    ),
    keep_together=False,
    parts=Parts(
        labels="alpha",
        parts=[
            Part(
                prompt=Text("State the natural domain of $f$."),
                answer=Math("(-infinity, +infinity)"),
                answer_space="0.6in",
            ),
            Part(
                prompt=Text(
                    "Investigate continuity at each boundary point. "
                    "Check the three conditions at every breakpoint."
                ),
                body=Parts(
                    labels="roman",
                    parts=[
                        Part(
                            prompt=Text(
                                "At $x = 0$, verify the three conditions for continuity:"
                            ),
                            body=Parts(
                                labels="numeric",
                                layout=PartsGrid(columns=3, answer_space="0.65in"),
                                parts=[
                                    Part(
                                        prompt=Math("lim_(x -> 0^-) f(x) ="),
                                        answer=Math("-1"),
                                    ),
                                    Part(
                                        prompt=Math("lim_(x -> 0^+) f(x) ="),
                                        answer=Math("1"),
                                    ),
                                    Part(
                                        prompt=Text("Is $f$ continuous at $x = 0$?"),
                                        answer=Text(
                                            "No — the one-sided limits disagree "
                                            "(jump discontinuity)."
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        Part(
                            prompt=Text(
                                "At a generic interior point $x = c > 0$, "
                                "verify continuity of the right branch:"
                            ),
                            body=Parts(
                                labels="numeric",
                                layout=PartsGrid(columns=2, answer_space="0.65in"),
                                parts=[
                                    Part(
                                        prompt=Math("lim_(x -> c^-) f(x) ="),
                                        answer=Math("2c + 1"),
                                    ),
                                    Part(
                                        prompt=Math("lim_(x -> c^+) f(x) ="),
                                        answer=Math("2c + 1"),
                                    ),
                                    Part(
                                        prompt=Math("f(c) ="),
                                        answer=Math("2c + 1"),
                                    ),
                                    Part(
                                        prompt=Text(
                                            "Continuous at every $c > 0$?"
                                        ),
                                        answer=Text("Yes — all three values agree."),
                                    ),
                                ],
                            ),
                        ),
                        Part(
                            prompt=Text(
                                "Summarize: list all discontinuities of $f$ "
                                "and classify each type."
                            ),
                            answer=Text(
                                "Jump discontinuity at $x = 0$; "
                                "$f$ is continuous everywhere else."
                            ),
                            answer_space="0.7in",
                        ),
                    ],
                ),
            ),
            Part(
                prompt=Text(
                    "Is $f$ integrable on $[-1, 3]$? Cite the relevant theorem."
                ),
                answer_space="0.7in",
            ),
        ],
    ),
    points=15,
))

# ===========================================================================
# P6  Outer 3-column grid with heterogeneous cell contents
#     Cell (a) is a FreeResponse leaf.
#     Cell (b) contains a nested roman Parts block — naturally taller.
#     Cell (c) is a FreeResponse leaf.
#     In LaTeX you would need manual minipage heights; Typst stretches grid
#     rows to fit the tallest cell automatically.
#
#     Tree: Block → Parts(PartsGrid(3), alpha)
#               ├── Part (a) → FreeResponse
#               ├── Part (b) → Parts(PartsGrid(1), roman)   ← taller cell
#               │                  ├── Part i   → FreeResponse
#               │                  ├── Part ii  → FreeResponse
#               │                  └── Part iii → FreeResponse
#               └── Part (c) → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text("Let $f(x) = x^4 - 8x^2$. Analyze its critical points."),
    parts=Parts(
        labels="alpha",
        layout=PartsGrid(columns=3, answer_space="1.1in"),
        parts=[
            Part(
                prompt=Text(
                    "Find all critical numbers by solving $f'(x) = 0$."
                ),
                answer=Math("x = 0, plus.minus 2"),
            ),
            Part(
                prompt=Text(
                    "Apply the Second Derivative Test to classify "
                    "each critical number."
                ),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=1, answer_space="0.45in"),
                    parts=[
                        Part(
                            prompt=Text(
                                "$f''(0) =$ ___, so $x = 0$ is a local ___."
                            ),
                            answer=Math('-16 < 0 => "local max"'),
                        ),
                        Part(
                            prompt=Text(
                                "$f''(2) =$ ___, so $x = 2$ is a local ___."
                            ),
                            answer=Math('32 > 0 => "local min"'),
                        ),
                        Part(
                            prompt=Text(
                                "$f''(-2) =$ ___, so $x = -2$ is a local ___."
                            ),
                            answer=Math('32 > 0 => "local min"'),
                        ),
                    ],
                ),
            ),
            Part(
                prompt=Text(
                    "State all local maximum and minimum values of $f$."
                ),
                answer=Math(
                    'f(0) = 0 quad "local max"; '
                    'f(plus.minus 2) = -16 quad "local min"'
                ),
            ),
        ],
    ),
    points=10,
))

# ===========================================================================
# P7  Outer 2-column grid where each cell is an inner 2-column grid
#     A grid of grids: in LaTeX this requires nested tabular environments with
#     hard-coded column widths.  Here it falls directly from
#     Part.body = Parts(PartsGrid(2)) inside Parts(PartsGrid(2)).
#     Both outer cells are symmetric, so the page looks balanced.
#
#     Tree: Block → Parts(PartsGrid(2), alpha)
#               ├── Part (a) → Parts(PartsGrid(2), roman)
#               │                  ├── Part i   → FreeResponse
#               │                  ├── Part ii  → FreeResponse
#               │                  ├── Part iii → FreeResponse
#               │                  └── Part iv  → FreeResponse
#               └── Part (b) → Parts(PartsGrid(2), roman)
#                                  ├── Part i   → FreeResponse
#                                  ├── Part ii  → FreeResponse
#                                  ├── Part iii → FreeResponse
#                                  └── Part iv  → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text(
        "Evaluate each function at the given inputs. "
        "The outer layout is a two-column grid; "
        "each column is itself organized as a two-column inner grid."
    ),
    parts=Parts(
        labels="alpha",
        layout=PartsGrid(columns=2, answer_space="0.55in"),
        parts=[
            Part(
                prompt=Math('f(x) = x^3 - 3x. quad "Evaluate:"'),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=2, answer_space="0.55in"),
                    parts=[
                        Part(prompt=Math("f(0) ="),       answer=Math("0")),
                        Part(prompt=Math("f(1) ="),       answer=Math("-2")),
                        Part(prompt=Math("f(-1) ="),      answer=Math("2")),
                        Part(prompt=Math("f(sqrt(3)) ="), answer=Math("0")),
                    ],
                ),
            ),
            Part(
                prompt=Math('g(x) = sin(pi x / 2). quad "Evaluate:"'),
                body=Parts(
                    labels="roman",
                    layout=PartsGrid(columns=2, answer_space="0.55in"),
                    parts=[
                        Part(prompt=Math("g(0) ="), answer=Math("0")),
                        Part(prompt=Math("g(1) ="), answer=Math("1")),
                        Part(prompt=Math("g(2) ="), answer=Math("0")),
                        Part(prompt=Math("g(3) ="), answer=Math("-1")),
                    ],
                ),
            ),
        ],
    ),
    points=8,
))

# ===========================================================================
# P8  indent=True vs indent=False on sibling parts at the same level
#     The indent flag lives on the Parts node and controls whether its block
#     is wrapped in #pad(left: 1.5em) by the renderer.
#     Part (a) uses indent=True  (default): sub-parts are pushed right 1.5 em.
#     Part (b) uses indent=False: sub-parts are flush with the parent prompt.
#     Part (c) uses indent=False: same, with three roman conditions.
#     Each setting is independent — it does not cascade to siblings or parents.
#
#     Tree: Block → Parts(alpha)
#               ├── Part (a) → Parts(roman, indent=True)   ← padded
#               │                  ├── Part i   → FreeResponse
#               │                  ├── Part ii  → FreeResponse
#               │                  └── Part iii → FreeResponse
#               ├── Part (b) → Parts(roman, indent=False)  ← flush
#               │                  ├── Part i   → FreeResponse
#               │                  └── Part ii  → FreeResponse
#               └── Part (c) → Parts(roman, indent=False)  ← flush
#                                  ├── Part i   → FreeResponse
#                                  ├── Part ii  → FreeResponse
#                                  └── Part iii → FreeResponse
# ===========================================================================
exam.add(MultipartProblem(
    prompt=Text("Give a precise definition for each property."),
    parts=Parts(
        labels="alpha",
        parts=[
            Part(
                prompt=Text("Continuity of $f$ at $x = c$:"),
                body=Parts(
                    labels="roman",
                    indent=True,
                    parts=[
                        Part(prompt=Text("$f(c)$ is defined.")),
                        Part(prompt=Text("$lim_(x -> c) f(x)$ exists.")),
                        Part(prompt=Text("$lim_(x -> c) f(x) = f(c)$.")),
                    ],
                ),
            ),
            Part(
                prompt=Text("Differentiability of $f$ at $x = c$:"),
                body=Parts(
                    labels="roman",
                    indent=False,
                    parts=[
                        Part(
                            prompt=Text(
                                "$f'(c) = lim_(h -> 0) (f(c+h) - f(c))/h$ "
                                "exists and is finite."
                            )
                        ),
                        Part(
                            prompt=Text(
                                "Note: differentiability implies continuity, "
                                "but not vice versa."
                            )
                        ),
                    ],
                ),
            ),
            Part(
                prompt=Text("Uniform continuity of $f$ on $(a, b)$:"),
                body=Parts(
                    labels="roman",
                    indent=True,
                    parts=[
                        Part(
                            prompt=Text(
                                "For every $epsilon > 0$ there exists $delta > 0$ such that"
                            )
                        ),
                        Part(
                            prompt=Math(
                                "forall x, y in (a, b): "
                                "|x - y| < delta => |f(x) - f(y)| < epsilon."
                            )
                        ),
                        Part(
                            prompt=Text(
                                "Key distinction: $delta$ depends only on $epsilon$, "
                                "not on the specific choice of $x$ or $y$."
                            )
                        ),
                    ],
                ),
            ),
        ],
    ),
    points=9,
))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
exam.build("out/showcase")
print("Built to out/showcase/")

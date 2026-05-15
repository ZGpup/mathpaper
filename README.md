# mathpaper

A math problem library and test builder for educators. Search a growing bank of tagged, curriculum-aligned problems, preview them rendered, and assemble a print-ready PDF quiz — without writing code. When you need a new problem type, write one Python function and it joins the library permanently.

---

## Setup

**Requirements:** [Typst](https://typst.app/) installed and on your PATH.

```bash
git clone https://github.com/your-username/mathpaper
cd mathpaper
conda env create -f environment.yml   # creates the mathpaper-dev environment
conda activate mathpaper-dev
```

For the browser test builder, also install the explore extras:

```bash
pip install ".[explore]"
```

Verify everything is working:

```bash
mathpaper check-typst
mathpaper index ./problems
```

---

## Browser test builder

The fastest way to build a quiz. No code required.

```bash
conda activate mathpaper-dev
mathpaper explore ./problems
```

This opens a local browser UI where you can:

- Search problems by topic, tag, course, difficulty, or keyword
- Preview any problem as a rendered PDF
- Select problems and arrange them into a test
- Set the title, course, and version
- Click **Build PDF** to produce student and answer-key PDFs in one step
- Click **Export .py** to get a Python script you can customize further

> Requires the `explore` extras (`pip install ".[explore]"`)

---

## Problem library

Problems are stored as tagged Python functions in the `problems/` directory. The library loads them at startup — no database to maintain, no migration scripts, just Python files you can version-control and share.

### Search from the command line

```bash
mathpaper search --tag derivatives
mathpaper search --topic "Implicit Differentiation" --difficulty hard
mathpaper search --course Calculus --keywords "critical points"
```

### Use from a script

```python
from mathpaper import Test
from mathpaper.library import ProblemLibrary

lib = ProblemLibrary("./problems")

quiz = Test(title="Derivatives Quiz", course="Calculus", version="A")
for p in lib.search(tags=["derivatives"]):
    quiz.add(p.build())

quiz.build("out/quiz")
# out/quiz/main.pdf        ← student version
# out/quiz/answer_key.pdf  ← answer key (computed, not hand-written)
```

Swap a problem's values without editing the library:

```python
from sympy import symbols
x = symbols("x")

lib.get("calc_deriv_poly_001").build(expr=x**3 - 3*x)
```

---

## Writing a new problem

Add a `@problem`-decorated function to any `.py` file under `problems/`. Run `mathpaper index ./problems` afterward and it appears in search immediately.

```python
# problems/calculus/derivatives.py
from mathpaper import Problem, Text, Math
from mathpaper.library import problem
from mathpaper.math.calculus import derivative
from mathpaper.math import sympy_to_typst
from sympy import symbols

x = symbols("x")

@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_001(expr=None):
    e = expr or x**4 - 8*x**2 + 7
    return Problem(
        prompt=Text(f"Let $f(x) = {sympy_to_typst(e)}$. Find $f'(x)$."),
        answer=Math(f"f'(x) = {sympy_to_typst(derivative(e))}"),
        answer_space="1.2in",
        points=4,
    )
```

The answer is computed from the expression — change `expr` and both the student worksheet and the answer key update automatically.

---

## Document structure

Every item added to a `Test` is a `Block`. The two convenience constructors are:

```python
Problem(prompt, answer_space="1in", answer=None, points=None)
MultipartProblem(prompt, parts, layout=None, figure=None, figure_layout=None, points=None)
```

Both return a `Block` — the single unified document node. The `body` of a `Block` is either a `FreeResponse` (leaf) or a `Parts` container (recursive).

### Flat multipart problem

```python
MultipartProblem(
    prompt=Text("Let $f(x) = x^2 - 4$. Answer the following."),
    parts=[
        Part("Find all real zeros.", answer=Math("x = -2, 2")),
        Part("Find the y-intercept.", answer=Math("(0, -4)")),
        Part("Describe the end behavior."),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=6,
)
```

### Nested sub-parts

`Part.body` can be another `Parts` container, creating an arbitrarily deep tree. Each `Parts` node carries its own label scheme (`"alpha"`, `"roman"`, or `"numeric"`) and optional grid layout. By default, nested parts are indented.

```python
MultipartProblem(
    prompt=Text("Let $f(x) = -2(x-3)^2 + 8$."),
    parts=[
        Part(
            prompt=Text("Find the key features of $f$."),
            body=Parts(
                labels="roman",
                layout=PartsGrid(columns=2, answer_space="0.9in"),
                parts=[
                    Part("State the vertex.", answer=Math("(3, 8)")),
                    Part("State the axis of symmetry.", answer=Math("x = 3")),
                    Part("Find the x-intercepts.", answer=Math("x = 1, 5")),
                    Part("Find the y-intercept.", answer=Math("(0, -10)")),
                ],
            ),
        ),
        Part(
            "State the range of $f$.",
            answer=Math("(-infinity, 8]"),
            answer_space="0.8in",
        ),
    ],
    layout=PartsGrid(columns=1, answer_space="0.8in"),
    points=10,
)
```

This renders as:

```
1.  Let f(x) = -2(x-3)² + 8.

    a.  Find the key features of f.

        ┌─────────────────────────┬─────────────────────────┐
        │ i.  State the vertex.   │ ii. State the axis …    │
        │                         │                         │
        │iii. Find the x-intercepts│ iv. Find the y-intercept│
        │                         │                         │
        └─────────────────────────┴─────────────────────────┘

    b.  State the range of f.
```

Set `indent=False` on any `Parts` node to suppress the automatic left-padding.

---

## Public API

```python
# Documents
Test(title, course="", version="")
Problem(prompt, answer=None, answer_space="1in", points=None, keep_together=True)
MultipartProblem(prompt, parts, layout=None, figure=None, figure_layout=None, points=None, keep_together=True)

# Core document node (returned by Problem and MultipartProblem)
Block(stem, body, answer=None, figure=None, figure_layout=None, points=None, keep_together=True)

# Part body types
FreeResponse(height="1in")
Parts(parts, layout=None, labels="alpha", indent=True)

# Parts
Part(prompt, body=None, answer=None, answer_space=None)
# body defaults to FreeResponse(answer_space or "1in")
# body can be FreeResponse or Parts for nested sub-parts

# Layout
PartsGrid(columns=1, answer_space="1in")
SideFigure(position="right", width="42%")
AnswerSpace(height="1in")

# Content
Text("plain text")
Math(r"x^2 - 4")          # Typst math syntax
RawTypst("#v(0.5in)")      # raw Typst escape hatch
Figure("path/to/file.svg")

# Problem library
ProblemLibrary("./problems")
@problem(id, tags, topic, description, difficulty, course)
lib.search(tags, topic, course, difficulty, keywords)
lib.get("problem_id").build(**kwargs)
lib.build_catalog("catalog.json")

# Renderer (advanced)
quiz.to_typst(mode="student")
quiz.write_typst(out_dir, mode)
quiz.build(out_dir)
```

### Label schemes

| `labels=`   | Output         |
|-------------|----------------|
| `"alpha"`   | a, b, c, …     |
| `"roman"`   | i, ii, iii, …  |
| `"numeric"` | 1, 2, 3, …     |

---

## Figures

The primary figure backend is **ManimCE**. Figures are rendered as static PNGs (last frame), white-background cropped, and cached in `.mathpaper_cache/figures/`.

```python
from mathpaper.figures.manim import ManimFigure
from manim import Scene, Circle, BLUE

class CircleFigure(ManimFigure):
    def __init__(self, width="60%"):
        class _Scene(Scene):
            def construct(self):
                self.add(Circle(color=BLUE))
        super().__init__(_Scene, "circle.png", width)
```

Skip re-rendering and use the cached version:

```bash
MATHPAPER_NO_RENDER_FIGURES=1 python my_quiz.py
# or
mathpaper build my_quiz.py --no-render-figures
```

Matplotlib SVG is also supported for simpler graphs (`mathpaper.figures.matplotlib`).

---

## Examples

| Example | File |
|---|---|
| Algebra 2 polynomial quiz (with nested sub-parts) | [examples/algebra_2/polynomial_quiz.py](examples/algebra_2/polynomial_quiz.py) |
| Calculus problem library | [problems/calculus/derivatives.py](problems/calculus/derivatives.py) |

```bash
python examples/algebra_2/polynomial_quiz.py
```

---

## Development

```bash
conda activate mathpaper-dev
pytest
ruff check src/
```

## License

GNU General Public License v3.0 (GPL-3.0)

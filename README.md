# mathpaper

Python-first math document generation. Define problems and their answers in Python, get a student worksheet and a correct answer key — both as PDFs.

```python
from mathpaper import Test, Problem, MultipartProblem, Part, Text, Math, PartsGrid
from sympy import symbols, expand, factor

x = symbols("x")
roots = [-3, 1, 4]
poly  = expand((x - roots[0]) * (x - roots[1]) * (x - roots[2]))

quiz = Test(title="Polynomial Quiz", course="Algebra 2", version="A")

quiz.add(Problem(
    prompt=Text(f"Factor completely: $x^2 - 3x - 10$"),
    answer=Math(str(factor(poly))),
    answer_space="1.2in",
    points=4,
))

quiz.build("out/quiz")
# out/quiz/main.pdf        ← student version
# out/quiz/answer_key.pdf  ← answer key (computed, not hand-written)
```

## Requirements

- Python 3.11+
- [Typst](https://typst.app/) on your PATH (for PDF compilation)

## Installation

**From source (development):**

```bash
git clone https://github.com/your-username/mathpaper
cd mathpaper
pip install -e ".[dev]"
```

Verify Typst is found:

```bash
mathpaper check-typst
```

## Quick start

### Simple worksheet

```python
from mathpaper import Test, Problem, Text, Math

quiz = Test(title="Linear Equations", course="Algebra 1")

quiz.add(Problem(
    prompt=Text("Solve for x:  2x + 5 = 13"),
    answer=Math("x = 4"),
    answer_space="1in",
    points=3,
))

quiz.build("out/my_quiz")
```

### Multi-part problem with auto-computed answers

```python
from mathpaper import Test, MultipartProblem, Part, Text, Math, PartsGrid
from sympy import symbols, expand, factor

x = symbols("x")

# Define roots once — answers fall out automatically
roots   = [-2, 5]
poly    = expand((x - roots[0]) * (x - roots[1]))
factored = factor(poly)
y_int   = int(poly.subs(x, 0))

quiz = Test(title="Quadratic Functions", course="Algebra 2")
quiz.add(MultipartProblem(
    prompt=Text(f"Let $f(x) = {poly}$."),
    parts=[
        Part("Find all real zeros.", answer=Math(", ".join(str(r) for r in sorted(roots)))),
        Part("Find the y-intercept.", answer=Math(f"(0, {y_int})")),
        Part("Write f in factored form.", answer=Math(str(factored))),
        Part("Describe the end behavior."),
    ],
    layout=PartsGrid(columns=2, answer_space="1.2in"),
    points=8,
))

quiz.build("out/quadratic_quiz")
```

### Output structure

```
out/quadratic_quiz/
  main.typ         ← Typst source, student version
  main.pdf
  answer_key.typ   ← Typst source, solution version
  answer_key.pdf
  assets/          ← figures copied here on build
  manifest.json    ← metadata
```

## Why Python → Typst?

- **Computed answers**: use SymPy, NumPy, or any math library to generate answers. The answer key is correct by construction.
- **Variants**: change roots or coefficients at the top of a script and regenerate 30 quiz versions without re-checking a single answer.
- **Figures**: pipe Matplotlib or custom SVG output directly into problems as assets (Phase 3).
- **Inspectable output**: generated `.typ` files are readable and debuggable. You are never locked into the Python layer.

## Public API

```python
# Documents
Test(title, course="", version="")
Problem(prompt, answer=None, answer_space=None, points=None)
MultipartProblem(prompt, parts, figure=None, figure_layout=None, layout=None, points=None)
Part(prompt, answer=None, answer_space=None)

# Layout
PartsGrid(columns=1, answer_space="1in")
SideFigure(position="right", width="42%")
AnswerSpace(height="1in")

# Content
Text("plain text")
Math(r"x^2 - 4")          # Typst math syntax
RawTypst("#v(0.5in)")      # raw Typst escape hatch
Figure("path/to/file.svg")

# Renderer (advanced)
TypstRenderer()
quiz.to_typst(mode="student")    # returns Typst string
quiz.write_typst(out_dir, mode)  # writes .typ file, returns Path
quiz.build(out_dir)              # full build: .typ + .pdf + assets + manifest
```

## Examples

| Example | File |
|---|---|
| Algebra 1 linear equations worksheet | [examples/algebra_1/build.py](examples/algebra_1/build.py) |
| Algebra 2 polynomial analysis quiz | [examples/algebra_2/polynomial_quiz.py](examples/algebra_2/polynomial_quiz.py) |

Run any example from the project root:

```bash
python examples/algebra_2/polynomial_quiz.py
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
```

## License

GNU General Public License v3.0 (GPL-3.0)

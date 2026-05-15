"""Tests for the Typst renderer."""
from mathpaper import (
    Math,
    MultipartProblem,
    Part,
    Parts,
    PartsGrid,
    Problem,
    RawTypst,
    SideFigure,
    Test,
    Text,
)
from mathpaper.figures.base import Figure
from mathpaper.render.escaping import escape_typst_text
from mathpaper.render.typst import TypstRenderer


def _render(test, mode="student"):
    return TypstRenderer().render(test, mode)


def test_problem_stem_appears_in_student_output():
    t = Test(title="T")
    t.add(Problem(prompt=Text("Find the answer."), answer=Math("42")))
    out = _render(t, mode="student")
    assert "Find the answer." in out
    # Answer must be hidden in student mode
    assert "Answer:" not in out
    assert "42" not in out


def test_problem_answer_appears_in_solution_mode():
    t = Test(title="T")
    t.add(Problem(prompt=Text("Find it."), answer=Math("42")))
    out = _render(t, mode="solution")
    assert "*Answer:*" in out
    assert "$42$" in out


def test_multipart_alpha_labels():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("Do these:"),
        parts=[Part("one"), Part("two"), Part("three")],
    ))
    out = _render(t)
    assert "*a.*" in out and "*b.*" in out and "*c.*" in out


def test_multipart_roman_labels():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=Parts(parts=[Part("p1"), Part("p2"), Part("p3")], labels="roman"),
    ))
    out = _render(t)
    assert "*i.*" in out and "*ii.*" in out and "*iii.*" in out


def test_multipart_numeric_labels():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=Parts(parts=[Part("a"), Part("b")], labels="numeric"),
    ))
    out = _render(t)
    assert "*1.*" in out and "*2.*" in out


def test_parts_grid_emits_grid_typst():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=[Part("a"), Part("b"), Part("c"), Part("d")],
        layout=PartsGrid(columns=2, answer_space="1.5in"),
    ))
    out = _render(t)
    assert "#grid(columns: (1fr, 1fr)" in out


def test_nested_parts_render_with_indent():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("outer"),
        parts=[
            Part(prompt=Text("a"), body=Parts(
                labels="roman",
                parts=[Part("inner1"), Part("inner2")],
            )),
        ],
    ))
    out = _render(t)
    assert "#pad(left: 1.5em)" in out
    assert "*i.*" in out and "*ii.*" in out


def test_nested_parts_indent_false_suppresses_pad():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("outer"),
        parts=[
            Part(prompt=Text("a"), body=Parts(
                labels="roman",
                indent=False,
                parts=[Part("inner1")],
            )),
        ],
    ))
    out = _render(t)
    assert "#pad(left: 1.5em)" not in out


def test_solution_part_shows_answer_block():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=[Part("p", answer=Math("99"))],
    ))
    out = _render(t, mode="solution")
    assert "$99$" in out
    assert "luma(230)" in out  # answer highlight block


def test_solution_part_without_answer_shows_blank_space():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=[Part("p", answer_space="2.5in")],
    ))
    out = _render(t, mode="solution")
    # No answer -> falls through to blank space
    assert "#v(2.5in)" in out


def test_points_appear_in_header_when_set():
    t = Test(title="T")
    t.add(Problem(prompt=Text("x"), points=7))
    out = _render(t)
    assert "(7 pts)" in out


def test_side_figure_layout_wraps_parts_in_two_column_grid():
    t = Test(title="T")
    t.add(MultipartProblem(
        prompt=Text("stem"),
        parts=[Part("a")],
        figure=Figure(path="assets/example.png", width="100%"),
        figure_layout=SideFigure(position="right", width="40%"),
    ))
    out = _render(t)
    assert "#grid(columns: (1fr, 40%)" in out
    assert '#image("assets/example.png"' in out


def test_raw_typst_passes_through_untouched():
    t = Test(title="T")
    t.add(Problem(prompt=RawTypst("#lorem(5)")))
    out = _render(t)
    assert "#lorem(5)" in out


def test_escape_typst_text_protects_inline_math():
    s = escape_typst_text("Find $x^2 + 1$ for #1.")
    assert "$x^2 + 1$" in s          # math region untouched
    assert "\\#1" in s                # '#' outside math is escaped


def test_escape_typst_text_escapes_specials_outside_math():
    s = escape_typst_text("[bracket] *star* _under_")
    assert "\\[" in s and "\\]" in s
    assert "\\*" in s
    assert "\\_" in s


def test_math_content_emits_dollar_delimited_typst():
    assert Math("x^2").to_typst() == "$x^2$"


def test_test_header_contains_title_course_version():
    t = Test(title="My Quiz", course="Algebra", version="A")
    out = _render(t)
    assert "My Quiz" in out
    assert "Algebra" in out
    assert "Version A" in out

"""Tests for the Block / Problem / MultipartProblem / Part / Parts model."""
from mathpaper import (
    Block,
    FreeResponse,
    Math,
    MultipartProblem,
    Part,
    Parts,
    PartsGrid,
    Problem,
    Text,
)


def test_problem_returns_block_with_free_response_body():
    b = Problem(prompt=Text("hi"), answer=Math("1"), answer_space="2in", points=3)
    assert isinstance(b, Block)
    assert isinstance(b.body, FreeResponse)
    assert b.body.height == "2in"
    assert b.points == 3
    assert b.answer is not None


def test_problem_keep_together_default_true():
    assert Problem(prompt=Text("x")).keep_together is True


def test_multipart_problem_returns_block_with_parts_body():
    b = MultipartProblem(
        prompt=Text("stem"),
        parts=[Part("a"), Part("b")],
        layout=PartsGrid(columns=2),
        points=5,
    )
    assert isinstance(b, Block)
    assert isinstance(b.body, Parts)
    assert len(b.body.parts) == 2
    assert b.body.layout.columns == 2
    assert b.points == 5


def test_multipart_problem_accepts_parts_object_directly():
    parts_node = Parts(parts=[Part("only")], labels="numeric")
    b = MultipartProblem(prompt=Text("stem"), parts=parts_node)
    assert b.body is parts_node


def test_part_answer_space_shorthand_initializes_free_response_body():
    p = Part("prompt", answer_space="0.8in")
    assert isinstance(p.body, FreeResponse)
    assert p.body.height == "0.8in"


def test_part_default_body_is_one_inch_free_response():
    p = Part("prompt")
    assert isinstance(p.body, FreeResponse)
    assert p.body.height == "1in"


def test_part_accepts_nested_parts_body():
    inner = Parts(parts=[Part("i"), Part("ii")], labels="roman")
    p = Part("outer", body=inner)
    assert p.body is inner


def test_parts_default_label_scheme_is_alpha_and_indented():
    p = Parts(parts=[])
    assert p.labels == "alpha"
    assert p.indent is True

"""End-to-end build tests: object model -> Typst source -> (optionally) PDF."""
import json
import shutil
from pathlib import Path

import pytest

from mathpaper import Math, MultipartProblem, Part, PartsGrid, Problem, Test, Text
from mathpaper.figures.base import Figure
from mathpaper.render.compiler import typst_available


@pytest.fixture
def simple_quiz():
    t = Test(title="Build Test", course="UnitTest", version="A")
    t.add(Problem(prompt=Text("What is $2+2$?"), answer=Math("4"), points=2))
    t.add(MultipartProblem(
        prompt=Text("Multipart."),
        parts=[
            Part("First.", answer=Math("x")),
            Part("Second.", answer=Math("y")),
        ],
        layout=PartsGrid(columns=2, answer_space="0.8in"),
        points=4,
    ))
    return t


def test_write_typst_creates_student_and_solution_files(simple_quiz, tmp_path):
    student = simple_quiz.write_typst(tmp_path, mode="student")
    solution = simple_quiz.write_typst(tmp_path, mode="solution")
    assert student.name == "main.typ"
    assert solution.name == "answer_key.typ"
    assert student.read_text().startswith("#set page(")
    assert solution.read_text().startswith("#set page(")


def test_build_writes_manifest_with_block_summary(simple_quiz, tmp_path):
    simple_quiz.build(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert manifest["title"] == "Build Test"
    assert manifest["course"] == "UnitTest"
    assert manifest["version"] == "A"
    assert len(manifest["problems"]) == 2
    assert manifest["problems"][0]["body"] == "FreeResponse"
    assert manifest["problems"][0]["points"] == 2
    assert manifest["problems"][1]["body"] == "Parts"
    assert manifest["problems"][1]["points"] == 4


def test_collect_assets_copies_top_level_figure(tmp_path):
    from mathpaper.render.assets import collect_assets
    src_fig = tmp_path / "src_figure.png"
    src_fig.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 64)

    t = Test(title="Figs")
    t.add(MultipartProblem(
        prompt=Text("With figure."),
        parts=[Part("a")],
        figure=Figure(path=str(src_fig), width="50%"),
    ))
    assets_dir = tmp_path / "assets"
    collect_assets(t._blocks, assets_dir)
    assert (assets_dir / "src_figure.png").exists()


def test_collect_assets_recurses_into_nested_parts(tmp_path):
    """Regression: collect_assets must recurse into nested Parts."""
    from mathpaper import Parts
    from mathpaper.render.assets import collect_assets

    src_fig = tmp_path / "nested_figure.png"
    src_fig.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 64)

    t = Test(title="Nested figs")
    t.add(MultipartProblem(
        prompt=Text("outer"),
        parts=[
            Part(
                prompt=Text("outer sub"),
                body=Parts(
                    parts=[Part("deep")],
                    labels="roman",
                ),
            ),
        ],
    ))
    inner_part = t._blocks[0].body.parts[0].body.parts[0]
    inner_part.figure = Figure(path=str(src_fig), width="50%")

    assets_dir = tmp_path / "assets"
    collect_assets(t._blocks, assets_dir)
    assert (assets_dir / "nested_figure.png").exists()


@pytest.mark.skipif(not typst_available(), reason="typst not on PATH")
def test_build_compiles_pdfs_when_typst_available(simple_quiz, tmp_path):
    simple_quiz.build(tmp_path)
    assert (tmp_path / "main.pdf").exists()
    assert (tmp_path / "answer_key.pdf").exists()
    assert (tmp_path / "main.pdf").stat().st_size > 0


def test_to_typst_is_pure(simple_quiz):
    """Calling to_typst twice should produce identical output."""
    a = simple_quiz.to_typst("student")
    b = simple_quiz.to_typst("student")
    assert a == b

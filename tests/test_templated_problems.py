"""Tests for the TemplatedProblem pipeline: decorator → staging → build."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from mathpaper import TemplatedProblem, Test
from mathpaper.library import ProblemLibrary
from mathpaper.render.compiler import typst_available


# ---------------------------------------------------------------------------
# Fixture: a minimal problem on disk so the @problem decorator can resolve its
# sibling .typ at decoration time.
# ---------------------------------------------------------------------------

_PY = textwrap.dedent(
    """
    from mathpaper import TemplatedProblem
    from mathpaper.library import problem

    @problem(
        id="demo_templated_001",
        tags=["unit"],
        topic="Demo",
        description="Templated demo problem",
        difficulty="easy",
        course="UnitTest",
    )
    def demo_templated_001(seed=None):
        return TemplatedProblem(
            points=5,
            context={"answer": "42"},
        )
    """
)

_TYP = textwrap.dedent(
    """
    #import "mathpaper.typ": *
    #let ctx = json("context.json")
    #problem(number: ctx.number, points: ctx.points)[
      What is the answer? #answer-space(0.5in)
      #if-solution[*Answer:* #ctx.answer]
    ]
    """
)


@pytest.fixture
def problem_dir(tmp_path: Path) -> Path:
    pdir = tmp_path / "problems"
    pdir.mkdir()
    (pdir / "demo_templated_001.py").write_text(_PY)
    (pdir / "demo_templated_001.typ").write_text(_TYP)
    return pdir


# ---------------------------------------------------------------------------
# Decorator + ProblemDef
# ---------------------------------------------------------------------------

def test_decorator_resolves_sibling_typ(problem_dir):
    lib = ProblemLibrary(problem_dir)
    defn = lib.get("demo_templated_001")
    assert defn.template_path is not None
    assert defn.template_path.name == "demo_templated_001.typ"
    assert defn.template_path.exists()


def test_build_returns_templatedproblem_with_template_filled(problem_dir):
    lib = ProblemLibrary(problem_dir)
    result = lib.get("demo_templated_001").build()
    assert isinstance(result, TemplatedProblem)
    assert result.template is not None
    assert Path(result.template).name == "demo_templated_001.typ"
    assert result.points == 5
    assert result.context == {"answer": "42"}


def test_decorator_raises_when_no_sibling_typ(tmp_path):
    """If no .typ sibling exists, decoration succeeds but build() raises."""
    pdir = tmp_path / "problems"
    pdir.mkdir()
    (pdir / "missing_template_001.py").write_text(
        textwrap.dedent(
            """
            from mathpaper import TemplatedProblem
            from mathpaper.library import problem

            @problem(id="missing_template_001", tags=[], topic="x",
                     description="x", difficulty="easy", course="x")
            def missing_template_001():
                return TemplatedProblem(context={})
            """
        )
    )
    lib = ProblemLibrary(pdir)
    with pytest.raises(FileNotFoundError):
        lib.get("missing_template_001").build()


# ---------------------------------------------------------------------------
# Staging
# ---------------------------------------------------------------------------

def test_stage_creates_subdir_with_problem_and_context(problem_dir, tmp_path):
    from mathpaper.render.templated import stage_templated_problem

    lib = ProblemLibrary(problem_dir)
    prob = lib.get("demo_templated_001").build()
    out = tmp_path / "out"
    out.mkdir()

    subdir_name = stage_templated_problem(prob, out, number=1)
    assert subdir_name == "problem_001"

    sub = out / subdir_name
    assert (sub / "problem.typ").exists()
    assert (sub / "context.json").exists()
    assert (sub / "mathpaper.typ").exists()

    ctx = json.loads((sub / "context.json").read_text())
    assert ctx["number"] == 1
    assert ctx["points"] == 5
    assert ctx["answer"] == "42"


def test_stage_does_not_overwrite_explicit_context_number(problem_dir, tmp_path):
    """If the author put 'number' or 'points' in the context, keep theirs."""
    from mathpaper.render.templated import stage_templated_problem

    lib = ProblemLibrary(problem_dir)
    prob = lib.get("demo_templated_001").build()
    prob.context["number"] = 99
    prob.context["points"] = 999
    out = tmp_path / "out"
    out.mkdir()

    stage_templated_problem(prob, out, number=1)
    ctx = json.loads((out / "problem_001" / "context.json").read_text())
    assert ctx["number"] == 99
    assert ctx["points"] == 999


# ---------------------------------------------------------------------------
# Test.build() end-to-end
# ---------------------------------------------------------------------------

def test_test_build_assembles_per_subdir_layout(problem_dir, tmp_path):
    lib = ProblemLibrary(problem_dir)
    quiz = Test(title="Templated Test", course="UT", version="A")
    quiz.add(lib.get("demo_templated_001").build())
    quiz.add(lib.get("demo_templated_001").build())  # twice, to check numbering

    out = tmp_path / "build"
    quiz.build(out)

    assert (out / "main.typ").exists()
    assert (out / "answer_key.typ").exists()
    assert (out / "mathpaper.typ").exists()
    assert (out / "problem_001" / "problem.typ").exists()
    assert (out / "problem_002" / "problem.typ").exists()
    assert (out / "manifest.json").exists()

    main_src = (out / "main.typ").read_text()
    assert '#include "problem_001/problem.typ"' in main_src
    assert '#include "problem_002/problem.typ"' in main_src
    assert "set-solution-mode(false)" in main_src

    key_src = (out / "answer_key.typ").read_text()
    assert "set-solution-mode(true)" in key_src


def test_test_add_rejects_non_templated_block():
    """Test.add only accepts TemplatedProblem — anything else is a TypeError."""
    quiz = Test(title="Bad")
    with pytest.raises(TypeError):
        quiz.add("not a problem")


def test_manifest_records_templated_problems(problem_dir, tmp_path):
    lib = ProblemLibrary(problem_dir)
    quiz = Test(title="T", course="UT")
    quiz.add(lib.get("demo_templated_001").build())
    quiz.build(tmp_path / "build")

    manifest = json.loads((tmp_path / "build" / "manifest.json").read_text())
    assert manifest["problems"][0]["points"] == 5
    assert manifest["problems"][0]["template"].endswith("demo_templated_001.typ")


@pytest.mark.skipif(not typst_available(), reason="typst not on PATH")
def test_templated_build_compiles_pdfs(problem_dir, tmp_path):
    lib = ProblemLibrary(problem_dir)
    quiz = Test(title="T", course="UT", version="A")
    quiz.add(lib.get("demo_templated_001").build())

    out = tmp_path / "build"
    quiz.build(out)

    assert (out / "main.pdf").exists()
    assert (out / "main.pdf").stat().st_size > 0
    assert (out / "answer_key.pdf").exists()

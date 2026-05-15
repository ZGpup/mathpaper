"""Tests for the @problem decorator and ProblemLibrary."""
import textwrap

import pytest

from mathpaper import Block
from mathpaper.library import ProblemLibrary, ProblemDef


_PROBLEM_FILE = textwrap.dedent("""
    from mathpaper import Problem, Text
    from mathpaper.library import problem

    @problem(
        id="test_p_001",
        tags=["unit", "demo"],
        topic="Demo",
        description="A demo problem",
        difficulty="easy",
        course="UnitTest",
    )
    def test_p_001(answer_text="hello"):
        return Problem(prompt=Text(answer_text))

    @problem(
        id="test_p_002",
        tags=["unit"],
        topic="Other",
        description="Another problem",
        difficulty="hard",
        course="UnitTest",
    )
    def test_p_002():
        return Problem(prompt=Text("static"))
""")


@pytest.fixture
def lib_dir(tmp_path):
    pdir = tmp_path / "problems"
    pdir.mkdir()
    (pdir / "demo.py").write_text(_PROBLEM_FILE)
    return pdir


def test_library_discovers_decorated_problems(lib_dir):
    lib = ProblemLibrary(lib_dir)
    ids = {p.id for p in lib.all()}
    assert ids == {"test_p_001", "test_p_002"}


def test_library_get_returns_problemdef(lib_dir):
    lib = ProblemLibrary(lib_dir)
    p = lib.get("test_p_001")
    assert isinstance(p, ProblemDef)
    assert p.topic == "Demo"
    assert p.difficulty == "easy"


def test_library_build_invokes_function_returns_block(lib_dir):
    lib = ProblemLibrary(lib_dir)
    block = lib.get("test_p_001").build()
    assert isinstance(block, Block)


def test_library_build_accepts_kwargs(lib_dir):
    lib = ProblemLibrary(lib_dir)
    block = lib.get("test_p_001").build(answer_text="custom")
    assert block.stem.body == "custom"


def test_search_filters_by_tag(lib_dir):
    lib = ProblemLibrary(lib_dir)
    results = lib.search(tags=["demo"])
    assert len(results) == 1
    assert results[0].id == "test_p_001"


def test_search_filters_by_difficulty(lib_dir):
    lib = ProblemLibrary(lib_dir)
    results = lib.search(difficulty="hard")
    assert len(results) == 1
    assert results[0].id == "test_p_002"


def test_search_filters_by_topic(lib_dir):
    lib = ProblemLibrary(lib_dir)
    results = lib.search(topic="Other")
    assert [r.id for r in results] == ["test_p_002"]


def test_search_filters_by_keyword(lib_dir):
    lib = ProblemLibrary(lib_dir)
    results = lib.search(keywords="another")
    assert len(results) == 1


def test_library_get_unknown_raises_keyerror(lib_dir):
    lib = ProblemLibrary(lib_dir)
    with pytest.raises(KeyError):
        lib.get("nope")


def test_build_catalog_writes_json(lib_dir, tmp_path):
    import json

    lib = ProblemLibrary(lib_dir)
    out = tmp_path / "catalog.json"
    lib.build_catalog(out)
    cat = json.loads(out.read_text())
    assert len(cat["problems"]) == 2
    assert {p["id"] for p in cat["problems"]} == {"test_p_001", "test_p_002"}

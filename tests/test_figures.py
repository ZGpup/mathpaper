"""Tests for figure base class and figure backends."""
import os

import matplotlib.pyplot as plt
import pytest

from mathpaper.figures.base import Figure
from mathpaper.figures.manim import ManimFigure, _cache_path
from mathpaper.figures.matplotlib import MatplotlibFigure


def test_figure_to_typst_emits_image_call():
    f = Figure(path="some/path/diagram.png", width="60%")
    out = f.to_typst()
    assert '#image("assets/diagram.png"' in out
    assert "width: 60%" in out


def test_matplotlib_figure_renders_svg_to_cache(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    f = MatplotlibFigure(fig, "line_plot.svg")
    assert f.path.endswith("line_plot.svg")
    assert (tmp_path / ".mathpaper_cache" / "figures" / "matplotlib" / "line_plot.svg").exists()


def test_manim_cache_path_is_namespaced_by_scene_class():
    class A: pass
    class B: pass
    pa = _cache_path(A, "fig.png")
    pb = _cache_path(B, "fig.png")
    assert pa != pb
    assert pa.name == "fig.png"
    assert pb.name == "fig.png"


def test_manim_no_render_env_uses_placeholder(monkeypatch, tmp_path):
    """When MATHPAPER_NO_RENDER_FIGURES=1 and no cache exists, a placeholder PNG is produced."""
    PIL = pytest.importorskip("PIL")  # placeholder generation needs Pillow

    class _NopScene:
        __qualname__ = "test_figures._NopScene"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MATHPAPER_NO_RENDER_FIGURES", "1")

    f = ManimFigure(_NopScene, "noop.png", width="50%")
    assert os.path.exists(f.path)
    assert f.path.endswith("noop.png")


def test_manim_uses_cached_file_when_present(monkeypatch, tmp_path):
    class _Cached:
        __qualname__ = "test_figures._Cached"

    monkeypatch.chdir(tmp_path)
    # Pre-populate the cache so ManimFigure doesn't try to import manim.
    cached = _cache_path(_Cached, "cached.png")
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 16)

    f = ManimFigure(_Cached, "cached.png")
    assert f.path == str(cached)

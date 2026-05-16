"""Tests for figure base class and figure backends."""
import os

import matplotlib.pyplot as plt
import pytest

from mathpaper.figures.base import Figure
from mathpaper.figures.manim import (
    ManimFigure,
    _cache_path,
    _content_cache_path,
    _resolve_cache_path,
)
from mathpaper.figures.matplotlib import MatplotlibFigure


def test_figure_to_typst_emits_image_call():
    f = Figure(path="some/path/diagram.png", width="60%")
    out = f.to_typst()
    assert '#image("assets/diagram.png"' in out
    assert "width: 60%" in out


def test_figure_asset_name_strips_content_hash_prefix():
    """16-hex-char + underscore prefix from the manim cache is stripped."""
    f = Figure(path="cache/d33a57ee0a0d5bf4_triangle.png")
    assert f.asset_name == "triangle.png"
    assert '#image("assets/triangle.png"' in f.to_typst()


def test_figure_asset_name_leaves_normal_names_alone():
    """A name that just happens to look hex-ish but isn't the right shape stays untouched."""
    assert Figure(path="cache/diagram.png").asset_name == "diagram.png"
    # Too short to be a hash prefix
    assert Figure(path="cache/abc_diagram.png").asset_name == "abc_diagram.png"
    # 16 chars but contains non-hex
    assert Figure(path="cache/zzzzzzzzzzzzzzzz_diagram.png").asset_name == "zzzzzzzzzzzzzzzz_diagram.png"


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


def _build_scene(a, b, label):
    """Factory that returns a scene class closing over a, b, label."""
    class _S:
        def construct(self):
            return (a, b, label)
    return _S


def test_content_cache_path_changes_with_closure_values():
    """Same construct body, different closure args → different cache paths."""
    s1 = _build_scene(2, 3, "x")
    s2 = _build_scene(4, 5, "x")
    p1 = _content_cache_path(s1, "fig.png")
    p2 = _content_cache_path(s2, "fig.png")
    assert p1 is not None and p2 is not None
    assert p1 != p2


def test_content_cache_path_stable_for_same_closure():
    """Identical inputs → identical cache path (deterministic)."""
    s1 = _build_scene(2, 3, "x")
    s2 = _build_scene(2, 3, "x")
    assert _content_cache_path(s1, "fig.png") == _content_cache_path(s2, "fig.png")


def test_content_cache_path_returns_none_without_construct():
    class _NoConstruct:
        pass
    assert _content_cache_path(_NoConstruct, "fig.png") is None


def test_resolve_falls_back_to_qualname_without_construct():
    class _NoConstruct:
        __qualname__ = "test_figures._NoConstruct"
    assert _resolve_cache_path(_NoConstruct, "fig.png") == _cache_path(_NoConstruct, "fig.png")


def test_manim_force_render_env_ignores_cache(monkeypatch, tmp_path):
    """MATHPAPER_FORCE_RENDER_FIGURES=1 bypasses the cache even if the file exists."""
    pytest.importorskip("PIL")

    class _ForceScene:
        __qualname__ = "test_figures._ForceScene"

    monkeypatch.chdir(tmp_path)
    # Pre-populate cache. Without the force env, ManimFigure should reuse this.
    cached = _resolve_cache_path(_ForceScene, "force.png")
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 16)

    # With force=1 and no manim available, ManimFigure tries to render and would
    # fail. Combining with NO_RENDER_FIGURES=1 makes it take the placeholder
    # branch instead, which proves the cached-hit branch was skipped.
    monkeypatch.setenv("MATHPAPER_FORCE_RENDER_FIGURES", "1")
    monkeypatch.setenv("MATHPAPER_NO_RENDER_FIGURES", "1")
    f = ManimFigure(_ForceScene, "force.png")
    assert os.path.exists(f.path)
    # Placeholder is a real PNG written by Pillow; the seed bytes above are 24 bytes.
    # If the cache was honored, the file would still be those 24 bytes.
    assert os.path.getsize(f.path) > 24

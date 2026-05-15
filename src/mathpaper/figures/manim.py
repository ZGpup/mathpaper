"""ManimCE-backed figure base class."""
import hashlib
import os
import shutil
import tempfile
from pathlib import Path
from typing import Type

from mathpaper.figures.base import Figure

_FIGURE_CACHE = Path(".mathpaper_cache/figures")


def _cache_path(scene_class: Type, filename: str) -> Path:
    # Namespace by scene class qualname so two figures with the same filename
    # don't collide. sha1[:12] gives 48 bits — negligible collision probability.
    ns = hashlib.sha1(scene_class.__qualname__.encode()).hexdigest()[:12]
    return _FIGURE_CACHE / ns / filename


def _make_placeholder(dest: Path) -> Path:
    """Write a gray placeholder PNG to dest and return dest."""
    from PIL import Image, ImageDraw, ImageFont

    dest.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (400, 200), color=(220, 220, 220))
    draw = ImageDraw.Draw(img)
    label = f"[figure: {dest.name}]"
    try:
        font = ImageFont.load_default(size=18)
        bbox = draw.textbbox((0, 0), label, font=font)
        x = (400 - (bbox[2] - bbox[0])) // 2
        y = (200 - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), label, fill=(100, 100, 100), font=font)
    except Exception:
        draw.text((20, 90), label, fill=(100, 100, 100))
    img.save(dest, format="PNG")
    return dest


class ManimFigure(Figure):
    """A Figure rendered from a ManimCE Scene as a static PNG (last frame).

    White background and whitespace cropping are applied automatically so the
    PNG asset contains only the diagram content plus a small padding border.

    Rendered files are cached in .mathpaper_cache/figures/<hash>/<filename>.
    The hash is derived from the scene class's qualified name, so two figures
    with the same filename but different scene classes will not collide. Set
    the env var MATHPAPER_NO_RENDER_FIGURES=1 (or use
    `mathpaper build --no-render-figures`) to skip re-rendering and reuse the
    cached PNG instead.

    Subclasses define the scene as an inner class inside __init__ so it can
    close over constructor parameters, then call super().__init__().

    Example::

        class MyFigure(ManimFigure):
            def __init__(self, param, width="80%"):
                class _Scene(Scene):
                    def construct(self):
                        ...  # param accessible via closure
                super().__init__(_Scene, "my_figure.png", width)
    """

    def __init__(self, scene_class: Type, filename: str, width: str = "80%"):
        cached = _cache_path(scene_class, filename)

        if cached.exists():
            super().__init__(path=str(cached), width=width)
            return

        if os.environ.get("MATHPAPER_NO_RENDER_FIGURES"):
            super().__init__(path=str(_make_placeholder(cached)), width=width)
            return

        try:
            from manim import tempconfig
        except ImportError as exc:
            raise ImportError(
                "ManimFigure requires ManimCE: pip install manim"
            ) from exc

        tmpdir = Path(tempfile.mkdtemp())
        stem = Path(filename).stem

        try:
            with tempconfig({
                "media_dir": str(tmpdir),
                "save_last_frame": True,
                "write_to_movie": False,
                "output_file": stem,
                "background_color": "#ffffff",
                "verbosity": "WARNING",
                "disable_caching": True,
            }):
                scene = scene_class()
                scene.render()

            # Sort by mtime so the most-recently-written PNG is last; this
            # avoids picking up thumbnails or partial frames Manim may write.
            pngs = sorted(tmpdir.rglob("*.png"), key=lambda p: p.stat().st_mtime)
            if not pngs:
                raise RuntimeError(
                    f"ManimFigure: no PNG produced by scene {scene_class.__name__!r}. "
                    "Ensure the scene calls self.add() with at least one mobject."
                )

            self._crop_whitespace(pngs[-1])
            cached.parent.mkdir(parents=True, exist_ok=True)
            # shutil.copy2 works across filesystems; Path.rename() does not.
            shutil.copy2(pngs[-1], cached)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

        super().__init__(path=str(cached), width=width)

    @staticmethod
    def _crop_whitespace(path: Path, padding: int = 24) -> None:
        """Trim near-white borders from a PNG in-place, leaving a small padding."""
        import numpy as np
        from PIL import Image

        # Convert to RGB: background is always forced white, so alpha is unused.
        img = Image.open(path).convert("RGB")
        arr = np.array(img)

        is_bg = (arr[:, :, 0] >= 250) & (arr[:, :, 1] >= 250) & (arr[:, :, 2] >= 250)
        content = ~is_bg

        rows = np.any(content, axis=1)
        cols = np.any(content, axis=0)
        if not rows.any():
            return  # Blank frame — leave untouched

        h, w = arr.shape[:2]
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]

        r0 = max(0, r0 - padding)
        r1 = min(h - 1, r1 + padding)
        c0 = max(0, c0 - padding)
        c1 = min(w - 1, c1 + padding)

        img.crop((c0, r0, c1 + 1, r1 + 1)).save(path, format="PNG")

"""Matplotlib-backed figure base class."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from mathpaper.figures.base import Figure

_FIGURE_CACHE = Path(".mathpaper_cache/figures")


class MatplotlibFigure(Figure):
    """A Figure whose content is rendered from a matplotlib Figure object.

    Subclasses build a matplotlib Figure in their __init__ and call
    super().__init__(mpl_fig, filename, width) to render it to SVG and
    register it as a Figure asset. Rendered SVGs are stored in
    .mathpaper_cache/figures/ (same scheme as ManimFigure) so they are
    discoverable by collect_assets() and reusable across builds.
    """

    def __init__(self, mpl_fig: "plt.Figure", filename: str, width: str = "80%"):
        cache_dir = _FIGURE_CACHE / "matplotlib"
        cache_dir.mkdir(parents=True, exist_ok=True)
        path = cache_dir / filename
        mpl_fig.savefig(path, format="svg", bbox_inches="tight")
        plt.close(mpl_fig)
        super().__init__(path=str(path), width=width)

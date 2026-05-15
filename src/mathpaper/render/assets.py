import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathpaper.figures.base import Figure


def collect_assets(blocks: list, assets_dir: Path) -> None:
    assets_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        _walk(block, assets_dir)


def _walk(node, assets_dir: Path) -> None:
    """Walk a Block or Part subtree and copy any Figure assets found."""
    from mathpaper.figures.base import Figure
    from mathpaper.document.parts import Parts

    figure = getattr(node, "figure", None)
    if isinstance(figure, Figure):
        _copy_figure(figure, assets_dir)

    body = getattr(node, "body", None)
    if isinstance(body, Parts):
        for part in body.parts:
            _walk(part, assets_dir)


def _copy_figure(figure: "Figure", assets_dir: Path) -> None:
    src = Path(figure.path)
    if src.exists():
        shutil.copy2(src, assets_dir / src.name)

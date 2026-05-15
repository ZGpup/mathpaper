import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathpaper.figures.base import Figure


def collect_assets(blocks: list, assets_dir: Path) -> None:
    assets_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        _copy_block_assets(block, assets_dir)


def _copy_block_assets(block, assets_dir: Path) -> None:
    from mathpaper.figures.base import Figure
    from mathpaper.document.parts import Parts

    figure = getattr(block, "figure", None)
    if isinstance(figure, Figure):
        _copy_figure(figure, assets_dir)

    # Walk into the Parts body to find any part-level figures
    body = getattr(block, "body", None)
    if isinstance(body, Parts):
        for part in body.parts:
            part_figure = getattr(part, "figure", None)
            if isinstance(part_figure, Figure):
                _copy_figure(part_figure, assets_dir)


def _copy_figure(figure: "Figure", assets_dir: Path) -> None:
    src = Path(figure.path)
    if src.exists():
        shutil.copy2(src, assets_dir / src.name)

from dataclasses import dataclass
from pathlib import Path

# A 16-lowercase-hex prefix followed by an underscore, produced by the
# content-addressed cache in figures/manim.py. Stripped at staging time so
# user-facing asset names stay clean.
_HEX = set("0123456789abcdef")


def _strip_content_hash_prefix(name: str) -> str:
    if len(name) > 17 and name[16] == "_" and all(c in _HEX for c in name[:16]):
        return name[17:]
    return name


@dataclass
class Figure:
    path: str | Path
    width: str = "100%"

    @property
    def asset_name(self) -> str:
        """Filename to use when staging this figure in an assets/ directory.

        Strips the leading content-hash prefix that ManimFigure adds to cache
        filenames, so the staged asset keeps the user-supplied name and
        overwrites cleanly across edits instead of accumulating orphans.
        """
        return _strip_content_hash_prefix(Path(self.path).name)

    def to_typst(self, mode: str = "student") -> str:
        return f'#image("assets/{self.asset_name}", width: {self.width})'

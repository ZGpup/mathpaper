from dataclasses import dataclass
from pathlib import Path


@dataclass
class Figure:
    path: str | Path
    width: str = "100%"

    def to_typst(self, mode: str = "student") -> str:
        name = Path(self.path).name
        return f'#image("assets/{name}", width: {self.width})'

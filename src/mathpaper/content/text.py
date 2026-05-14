from dataclasses import dataclass
from mathpaper.render.escaping import escape_typst_text


@dataclass
class Text:
    body: str

    def to_typst(self, mode: str = "student") -> str:
        return escape_typst_text(self.body)

from dataclasses import dataclass, field


@dataclass
class AnswerSpace:
    height: str = "1in"

    def to_typst(self, mode: str = "student") -> str:
        if mode == "solution":
            return ""
        return f"#v({self.height})"


@dataclass
class PartsGrid:
    columns: int = 1
    answer_space: str = "1in"


@dataclass
class SideFigure:
    position: str = "right"
    width: str = "42%"

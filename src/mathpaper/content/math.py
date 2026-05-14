from dataclasses import dataclass


@dataclass
class Math:
    expr: str

    def to_typst(self, mode: str = "student") -> str:
        return f"${self.expr}$"

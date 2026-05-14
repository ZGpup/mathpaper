from dataclasses import dataclass


@dataclass
class RawTypst:
    source: str

    def to_typst(self, mode: str = "student") -> str:
        return self.source

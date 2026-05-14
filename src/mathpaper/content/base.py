from typing import Protocol, runtime_checkable


@runtime_checkable
class Content(Protocol):
    def to_typst(self, mode: str = "student") -> str: ...

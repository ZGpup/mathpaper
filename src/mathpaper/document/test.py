from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Test:
    title: str
    course: str = ""
    version: str = ""
    _blocks: list[Any] = field(default_factory=list, repr=False)

    # Tell pytest this is not a test class.
    __test__ = False

    def add(self, block: Any) -> None:
        self._blocks.append(block)

    def to_typst(self, mode: str = "student") -> str:
        from mathpaper.render.typst import TypstRenderer
        return TypstRenderer().render(self, mode)

    def write_typst(self, out_dir: str | Path, mode: str = "student") -> Path:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        name = "main" if mode == "student" else "answer_key"
        path = out / f"{name}.typ"
        path.write_text(self.to_typst(mode), encoding="utf-8")
        return path

    def build(self, out_dir: str | Path) -> None:
        from mathpaper.render.compiler import compile_typst, typst_available
        from mathpaper.render.assets import collect_assets

        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        assets_dir = out / "assets"

        collect_assets(self._blocks, assets_dir)

        student_typ = self.write_typst(out, mode="student")
        key_typ = self.write_typst(out, mode="solution")

        if typst_available():
            compile_typst(student_typ, out / "main.pdf")
            compile_typst(key_typ, out / "answer_key.pdf")
        else:
            print("Warning: typst not found on PATH — skipping PDF compilation.")

        self._write_manifest(out)

    def _write_manifest(self, out: Path) -> None:
        import mathpaper
        manifest = {
            "title": self.title,
            "course": self.course,
            "version": self.version,
            "created_by": f"mathpaper {mathpaper.__version__}",
            "problems": [
                {
                    "index": i + 1,
                    "body": type(getattr(b, "body", b)).__name__,
                    "points": getattr(b, "points", None),
                }
                for i, b in enumerate(self._blocks)
            ],
        }
        (out / "manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )

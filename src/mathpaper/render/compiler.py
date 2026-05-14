import subprocess
from pathlib import Path


def compile_typst(typ_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        ["typst", "compile", str(typ_path), str(pdf_path)],
        check=True,
    )


def typst_available() -> bool:
    try:
        subprocess.run(["typst", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

import re

_TYPST_SPECIAL = str.maketrans({
    "\\": "\\\\",
    "#":  "\\#",
    "@":  "\\@",
    "<":  "\\<",
    ">":  "\\>",
    "*":  "\\*",
    "_":  "\\_",
    "`":  "\\`",
    "~":  "\\~",
    "[":  "\\[",
    "]":  "\\]",
})

# Matches inline math regions $...$ so their contents are not escaped.
_MATH_RE = re.compile(r'(\$[^$]+\$)')


def escape_typst_text(text: str) -> str:
    """Escape Typst special characters, leaving $...$ math regions untouched."""
    parts = _MATH_RE.split(text)
    return "".join(
        part if part.startswith("$") else part.translate(_TYPST_SPECIAL)
        for part in parts
    )

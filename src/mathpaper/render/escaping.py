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


def escape_typst_text(text: str) -> str:
    return text.translate(_TYPST_SPECIAL)

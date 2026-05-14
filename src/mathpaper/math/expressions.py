"""Mathematical expressions and SymPy → Typst math conversion.

No mature LaTeX→Typst Python library exists yet (SymPy's Typst printer is
in development as of 2025). This module owns a growing fixup layer over
SymPy's latex() output. Add fixups here as new math domains are needed.
"""
import re

from sympy import latex


def sympy_to_typst(expr) -> str:
    """Convert a SymPy expression to a Typst math string.

    Strategy: SymPy → latex() → regex fixups → Typst.
    Covers polynomials, fractions, roots, and Greek letters.
    Extend the fixup list as new expression types are needed.
    """
    s = latex(expr)

    # Sizing delimiters — Typst doesn't use \left/\right
    s = s.replace(r"\left(", "(").replace(r"\right)", ")")
    s = s.replace(r"\left|", "|").replace(r"\right|", "|")

    # Roots: \sqrt{x} → sqrt(x)  (before exponents so sqrt{x^{2}} still works)
    s = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', s)

    # Exponents: x^{2} → x^2, x^{10} → x^(10)
    s = re.sub(r'\^\{(\w)\}', r'^\1', s)
    s = re.sub(r'\^\{([^}]+)\}', r'^(\1)', s)

    # Subscripts: x_{i} → x_i, x_{ij} → x_(ij)
    s = re.sub(r'_\{(\w)\}', r'_\1', s)
    s = re.sub(r'_\{([^}]+)\}', r'_(\1)', s)

    # Fractions: \frac{a}{b} → (a)/(b)
    # Runs after exponent/subscript fixups so denominators like x + 3 y^{2}
    # have already had their inner braces removed and are matchable.
    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)

    # Greek letters: \alpha → alpha (strip backslash)
    _greek = (
        "alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|"
        "nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|"
        "Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|"
        "Nu|Xi|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega"
    )
    s = re.sub(rf'\\({_greek})\b', r'\1', s)

    return s

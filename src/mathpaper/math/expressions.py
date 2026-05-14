"""Mathematical expressions and SymPy → Typst math conversion.

No mature LaTeX→Typst Python library exists yet (SymPy's Typst printer is
in development as of 2025). This module owns a growing fixup layer over
SymPy's latex() output. Add fixups here as new math domains are needed.
"""
import re

from sympy import latex


def _convert_fracs(s: str) -> str:
    """Replace all \\frac{A}{B} with (A)/(B) using proper brace matching.

    The simple regex approach breaks when A or B contain nested braces (e.g.
    log arguments, exponents that weren't cleaned up). This walks the string
    character by character to match balanced braces correctly.
    """
    result = []
    i = 0
    while i < len(s):
        if s[i:i+6] == r'\frac{':
            # find end of numerator brace group
            depth, j = 0, i + 5
            while j < len(s):
                if s[j] == '{':
                    depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            num_end = j
            num = s[i + 6 : num_end]

            # denominator brace group must follow immediately
            if num_end + 1 < len(s) and s[num_end + 1] == '{':
                depth, k = 0, num_end + 1
                while k < len(s):
                    if s[k] == '{':
                        depth += 1
                    elif s[k] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                den = s[num_end + 2 : k]
                result.append(f'({num})/({den})')
                i = k + 1
                continue

        result.append(s[i])
        i += 1
    return ''.join(result)


def _strip_func_braces(s: str, func_re) -> str:
    """Strip outer braces from \\funcname{arg} patterns using balanced brace matching.

    Handles subscripts like \\log_{5}{arg} and recursively processes nested
    function calls so inner \\sin{(x)} inside a \\log{...} are also stripped.
    """
    result = []
    i = 0
    while i < len(s):
        m = func_re.search(s, i)
        if not m:
            result.append(s[i:])
            break
        result.append(s[i:m.start()])
        func_name = m.group(1)
        subscript = m.group(2)
        depth = 1
        j = m.end()
        while j < len(s) and depth > 0:
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
            j += 1
        inner = s[m.end():j - 1]
        inner = _strip_func_braces(inner, func_re)
        result.append(f'{func_name}{subscript}{inner}')
        i = j
    return ''.join(result)


def _handle_log_base(expr) -> str | None:
    """If expr is log(X)/log(b), return the Typst 'log_b(X)' string, else None.

    SymPy stores log(X, b) as log(X)/log(b) internally. This detects that
    pattern and renders it in Typst subscript notation instead of a fraction.
    """
    from sympy import Mul, Pow, log as _log
    if not isinstance(expr, Mul):
        return None
    log_numer = None
    log_denom = None
    for arg in expr.args:
        if isinstance(arg, _log) and len(arg.args) == 1:
            log_numer = arg.args[0]
        elif (isinstance(arg, Pow) and
              isinstance(arg.args[0], _log) and
              len(arg.args[0].args) == 1 and
              arg.args[1] == -1):
            log_denom = arg.args[0].args[0]
        else:
            return None
    if log_numer is None or log_denom is None:
        return None
    base_str = sympy_to_typst(log_denom)
    inner_str = sympy_to_typst(log_numer)
    sub = f'_({base_str})' if len(base_str) > 1 else f'_{base_str}'
    return f'log{sub}({inner_str})'


def sympy_to_typst(expr) -> str:
    """Convert a SymPy expression to a Typst math string.

    Strategy: SymPy → latex() → fixups → Typst.
    Covers polynomials, fractions, roots, logs, trig, and Greek letters.
    Extend the fixup list as new expression types are needed.
    """
    result = _handle_log_base(expr)
    if result is not None:
        return result

    s = latex(expr)

    # Sizing delimiters — Typst doesn't use \left/\right.
    # SymPy sometimes emits \left ( (with a space) so use regex.
    s = re.sub(r'\\left\s*\(', '(', s)
    s = re.sub(r'\\right\s*\)', ')', s)
    s = re.sub(r'\\left\s*\[', '[', s)
    s = re.sub(r'\\right\s*\]', ']', s)
    s = re.sub(r'\\left\s*\|', '|', s)
    s = re.sub(r'\\right\s*\|', '|', s)

    # SymPy may use \operatorname{asin} etc. instead of \arcsin.
    for _op, _arc in [
        ('asin', 'arcsin'), ('acos', 'arccos'), ('atan', 'arctan'),
        ('acot', 'arccot'), ('asec', 'arcsec'), ('acsc', 'arccsc'),
    ]:
        s = s.replace(f'\\operatorname{{{_op}}}', f'\\{_arc}')

    # Math functions: strip \cmd{...} braces using balanced brace matching so
    # that complex nested arguments (fractions, exponents) are handled correctly.
    # Must run before _convert_fracs so these braces don't confuse frac parsing.
    _funcs = (
        "log|ln|exp|"
        "sin|cos|tan|cot|sec|csc|"
        "arcsin|arccos|arctan|arccot|arcsec|arccsc|"
        "sinh|cosh|tanh|coth"
    )
    _func_re = re.compile(rf'\\({_funcs})((?:_\{{[^}}]*\}}|_\w)*)\{{')
    s = _strip_func_braces(s, _func_re)
    # Also handle bare \cmd without braces (e.g. \log x)
    s = re.sub(rf'\\({_funcs})\b', r'\1', s)

    # Multiplication dot: \cdot → space (juxtaposition is multiplication in Typst)
    s = s.replace(r'\cdot', ' ')

    # Fractions: \frac{A}{B} → (A)/(B), handles nested braces.
    # Must run before exponents so ^{\frac{3}{2}} → ^{(3)/(2)} → ^((3)/(2)).
    s = _convert_fracs(s)

    # Exponents: ^{2} → ^2, ^{10} → ^(10).
    # Must run before sqrt so \sqrt{1 - x^{2}} → \sqrt{1 - x^2} → sqrt(1 - x^2).
    s = re.sub(r'\^\{(\w)\}', r'^\1', s)
    s = re.sub(r'\^\{([^}]+)\}', r'^(\1)', s)

    # Subscripts: x_{i} → x_i, x_{ij} → x_(ij)
    s = re.sub(r'_\{(\w)\}', r'_\1', s)
    s = re.sub(r'_\{([^}]+)\}', r'_(\1)', s)

    # Roots: now that nested ^{} are resolved, content is brace-free.
    s = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', s)

    # Trig powers: \arccos^{2}{\left(x\right)} → after prior steps becomes
    # arccos^2{(x)}. Strip the leftover {(...)} grouping.
    s = re.sub(r'(\w+)(\^[\w(][^{]*)\{(\([^){}]*\))\}', r'\1\2\3', s)

    # Greek letters: \alpha → alpha (strip backslash)
    _greek = (
        "alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|"
        "nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|"
        "Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|"
        "Nu|Xi|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega"
    )
    s = re.sub(rf'\\({_greek})\b', r'\1', s)

    # Strip spaces immediately inside parens — artifact of SymPy's \left ( ... \right )
    s = re.sub(r'\(\s+', '(', s)
    s = re.sub(r'\s+\)', ')', s)

    return s

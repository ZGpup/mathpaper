# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-13

### Added

**Core document model**
- `Test` — top-level document class with `.add()`, `.to_typst(mode)`, `.write_typst(out_dir, mode)`, and `.build(out_dir)`; writes `main.typ`, `answer_key.typ`, `main.pdf`, `answer_key.pdf`, `assets/`, and `manifest.json`
- `Problem` — single free-response problem with prompt, optional answer, answer space, and point value
- `MultipartProblem` — multi-part problem with prompt, parts list, optional figure, figure layout, and grid layout
- `Part` — individual part with prompt, optional answer, and per-part answer space override
- `AnswerSpace` — inline vertical space that disappears in solution mode
- `PartsGrid` — layout descriptor for multi-column part grids
- `SideFigure` — layout descriptor for side-by-side figure/content placement

**Content objects**
- `Text` — plain text content with Typst character escaping
- `Math` — Typst math expression rendered as inline `$...$`
- `RawTypst` — escape hatch for raw Typst source passthrough
- `Content` protocol — structural typing for all content objects

**Figure support**
- `Figure` — wraps an asset path; copied into `assets/` on build and referenced as `#image(...)` in Typst

**Renderer**
- `TypstRenderer` — generates standalone, readable Typst source from a `Test` object; handles page setup, header with name line, numbered problems, two-column part grids, and answer-key highlighting
- `escape_typst_text` — escapes `#`, `@`, `<`, `>`, `*`, `_`, `` ` ``, `\`, `~`, `[`, `]` in user text
- `compile_typst` — subprocess wrapper around `typst compile`; raises on failure
- `typst_available` — checks whether `typst` is on PATH before attempting compilation
- `collect_assets` — walks document blocks, finds `Figure` objects, and copies them into the output `assets/` directory

**Templates**
- `templates/typst/lib.typ` — stub template file; will grow into a macro library in Phase 2

**CLI**
- `mathpaper check-typst` — verifies that `typst` is installed and prints its version

**Examples**
- `examples/algebra_1/build.py` — linear equations worksheet demonstrating `Problem` and `MultipartProblem` with a 2-column `PartsGrid`
- `examples/algebra_2/polynomial_quiz.py` — polynomial analysis quiz using SymPy to compute factored forms, zeros, y-intercepts, end behavior, and positive intervals; answer key is correct by construction from the root definitions



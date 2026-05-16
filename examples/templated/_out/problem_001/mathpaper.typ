// mathpaper Typst helper library
//
// Imported by problem .typ files via:
//   #import "mathpaper.typ": *
//
// Provides the small set of layout primitives that mirror the (former) Python
// recursive-block model: numbered problems, multi-column parts grids, answer
// spaces that collapse in solution mode, side figures, and a helper to
// evaluate a context-supplied math string as live Typst math.

// ---------------------------------------------------------------------------
// Solution mode
// ---------------------------------------------------------------------------
// A single state cell driven by the master document; problems read it via
// #if-solution[...] and #answer-space() to switch between student and key.

#let _solution-mode = state("mp-solution-mode", false)

#let set-solution-mode(value) = _solution-mode.update(value)

#let if-solution(body) = context if _solution-mode.get() {
  set text(fill: rgb("#1d4ed8"))
  body
}

// ---------------------------------------------------------------------------
// Problem wrapper
// ---------------------------------------------------------------------------

#let problem(number: none, points: none, keep-together: true, body) = {
  let header = if number != none and points != none {
    [*#number. (#points pts)* ]
  } else if number != none {
    [*#number.* ]
  } else if points != none {
    [*(#points pts)* ]
  } else {
    []
  }
  let content = [#header #body]
  if keep-together {
    block(breakable: false, content)
  } else {
    content
  }
}

// ---------------------------------------------------------------------------
// Answer space (collapses in solution mode)
// ---------------------------------------------------------------------------

#let answer-space(height) = context if _solution-mode.get() {
  // No vertical space in the answer key — the answer itself fills the slot.
} else {
  v(height)
}

// ---------------------------------------------------------------------------
// Parts grid
// ---------------------------------------------------------------------------
// Multi-column parts with auto-labels. For single-column sequential parts use
// Typst's native `+` enum with `#set enum(numbering: "a.")` — that handles
// indentation and labeling natively at any nesting depth.

#let parts-grid(
  numbering: "a.",
  columns: 2,
  column-gutter: 1em,
  row-gutter: 0.8em,
  parts,
) = {
  let labeled = parts.enumerate().map(((i, body)) => {
    let label = std.numbering(numbering, i + 1)
    [*#label* #body]
  })
  grid(
    columns: columns,
    column-gutter: column-gutter,
    row-gutter: row-gutter,
    ..labeled,
  )
}

// ---------------------------------------------------------------------------
// Side figure
// ---------------------------------------------------------------------------
// Place a figure beside body content. `figure` is any Typst content (typically
// #image(...) from a context-supplied path).

#let side-figure(
  figure,
  position: right,
  width: 42%,
  gutter: 1em,
  body,
) = {
  let main-width = 100% - width - gutter
  if position == right {
    grid(
      columns: (main-width, width),
      column-gutter: gutter,
      body,
      figure,
    )
  } else {
    grid(
      columns: (width, main-width),
      column-gutter: gutter,
      figure,
      body,
    )
  }
}

// ---------------------------------------------------------------------------
// Math from string
// ---------------------------------------------------------------------------
// Render a context-supplied Typst-math string as live math. Use this for
// answers computed in Python and shipped via context.json — e.g.
//   #if-solution[*Answer:* #math-from-str(ctx.answers.derivative)]

#let math-from-str(s) = eval(s, mode: "math")

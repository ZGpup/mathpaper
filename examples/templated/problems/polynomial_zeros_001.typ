// Polynomial analysis problem — deep recursive parts.
//
// Demonstrates how Typst's native `+` enum handles nested parts with
// per-level numbering schemes (alpha → roman → numeric). The `parts-grid`
// helper is used at one level to lay sub-parts out side-by-side.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $#math-from-str(ctx.polynomial)$.

  #set enum(numbering: "a.")
  + Find all real zeros of $f$.
    #answer-space(0.8in)
    #if-solution[*Answer:* #math-from-str(ctx.answers.zeros)]

  + Determine the following key features:
    #parts-grid(numbering: "i.", columns: 2, (
      [
        The y-intercept.
        #answer-space(0.6in)
        #if-solution[*Answer:* #math-from-str(ctx.answers.y_intercept)]
      ],
      [
        Where $f(x) > 0$.
        #answer-space(0.6in)
        #if-solution[*Answer:* #math-from-str(ctx.answers.positive_intervals)]
      ],
    ))

  + Describe the end behavior of $f$:
    #set enum(numbering: "i.")
    + As $x -> -infinity$:
      #answer-space(0.5in)
      #if-solution[*Answer:* #math-from-str(ctx.answers.end_behavior_left)]
    + As $x -> +infinity$:
      #answer-space(0.5in)
      #if-solution[*Answer:* #math-from-str(ctx.answers.end_behavior_right)]
]

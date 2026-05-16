// Find f'(x), f''(x), and classify critical points for a degree-4 polynomial.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $#math-from-str(ctx.polynomial)$. Answer each question below.

  #parts-grid(numbering: "a.", columns: 2, (
    [
      Find $f'(x)$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.first_deriv)$]
    ],
    [
      Find $f''(x)$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.second_deriv)$]
    ],
    [
      Find all critical points of $f$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.critical_points)$]
    ],
    [
      Classify each critical point as a local min, local max, or neither.
      #answer-space(1.2in)
    ],
  ))
]

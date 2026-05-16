// Multipart analysis of a cubic: zeros, y-intercept, end behavior, positive intervals, turning points.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $#math-from-str(ctx.polynomial)$. Use algebra to answer the following.

  #parts-grid(numbering: "a.", columns: 2, (
    [
      Find all real zeros of $f$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.zeros)$]
    ],
    [
      Find the $y$-intercept.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.y_intercept)$]
    ],
    [
      Describe the end behavior of $f$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.end_behavior)$]
    ],
    [
      State the interval(s) where $f(x) > 0$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.positive_intervals)$]
    ],
    [
      What is the maximum number of turning points $f$ can have?
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.max_turning_points)$]
    ],
  ))
]

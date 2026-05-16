// Multipart analysis of a quadratic: zeros, y-intercept, end behavior, negative intervals.

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
      State the interval(s) where $f(x) < 0$.
      #answer-space(1.2in)
      #if-solution[*Answer:* $#math-from-str(ctx.answers.negative_intervals)$]
    ],
  ))
]

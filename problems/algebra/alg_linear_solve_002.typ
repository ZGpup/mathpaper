// Solve a linear equation requiring distribution.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Solve for $x$: $#math-from-str(ctx.equation)$

  #answer-space(1in)
  #if-solution[*Answer:* $#math-from-str(ctx.answers.x)$]
]

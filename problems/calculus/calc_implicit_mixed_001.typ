// Implicit differentiation of a complex mixed-exponent curve.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Given $#math-from-str(ctx.equation)$, use implicit differentiation to find
  $(d y)/(d x)$.

  #answer-space(2.5in)
  #if-solution[*Answer:* $#math-from-str(ctx.answers.dydx)$]
]

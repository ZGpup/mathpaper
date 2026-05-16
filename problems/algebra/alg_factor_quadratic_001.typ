// Factor a quadratic with a leading coefficient completely.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Factor completely: $#math-from-str(ctx.polynomial)$

  #answer-space(1.2in)
  #if-solution[*Answer:* $#math-from-str(ctx.answers.factored)$]
]

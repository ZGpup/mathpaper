// Find f'(x) for a degree-4 polynomial.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $#math-from-str(ctx.polynomial)$. Find $f'(x)$.

  #answer-space(1.2in)
  #if-solution[*Answer:* $#math-from-str(ctx.answers.derivative)$]
]

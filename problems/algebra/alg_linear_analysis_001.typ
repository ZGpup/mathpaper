// Slope-intercept analysis: slope, y-intercept, graph, solve for x.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Consider the equation $#math-from-str(ctx.equation)$.

  #set enum(numbering: "a.")
  + Find the slope.
    #answer-space(1in)
    #if-solution[*Answer:* $#math-from-str(ctx.answers.slope)$]

  + Find the $y$-intercept.
    #answer-space(1in)
    #if-solution[*Answer:* $#math-from-str(ctx.answers.y_intercept)$]

  + Graph the equation on the axes below.
    #answer-space(1.5in)

  + Find $x$ when $y = #ctx.y_target$.
    #answer-space(1in)
    #if-solution[*Answer:* $#math-from-str(ctx.answers.x_solve)$]
]

// Curve analysis: increasing/decreasing intervals, concavity, critical point classification.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Given $#math-from-str(ctx.polynomial)$, answer the following.

  #set enum(numbering: "a.")
  + Find the intervals on which $f$ is increasing and decreasing.
    Identify the $x$-values of any critical points.
    #answer-space(1.5in)
    #if-solution[
      *Increasing:* $#math-from-str(ctx.answers.increasing)$ \
      *Decreasing:* $#math-from-str(ctx.answers.decreasing)$ \
      *Critical points:* $#math-from-str(ctx.answers.critical_points)$
    ]

  + Find the intervals on which $f$ is concave up and concave down.
    Identify the $x$-values of any inflection points.
    #answer-space(1.5in)
    #if-solution[
      *Concave up:* $#math-from-str(ctx.answers.concave_up)$ \
      *Concave down:* $#math-from-str(ctx.answers.concave_down)$ \
      *Inflection points:* $#math-from-str(ctx.answers.inflection_points)$
    ]

  + Which critical points are local maxima, local minima, or neither?
    #answer-space(1.5in)
    #if-solution[*Answer:* $#math-from-str(ctx.answers.classifications)$]
]

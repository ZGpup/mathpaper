// Triangle related-rates problem.
//
// Open this file in VSCode with Tinymist for full math highlighting,
// autocomplete, and live preview. Python (triangle_rate_001.py) computes
// the figure and the answer expressions and ships them via context.json.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  The area of a triangle with sides $a$ and $b$ and included angle $theta$
  is $A = 1/2 a b sin(theta)$.

  #side-figure(image(ctx.figure, width: 100%), position: right, width: 35%)[
    + If $a = 2$, $b = 3$, and $theta$ is increasing at
      $(d theta) / (d t) = 0.2$ rad\/s, find a formula for
      $(d A) / (d t)$ in terms of $theta$.

      #answer-space(1.6in)
      #if-solution[
        *Answer:* #math-from-str(ctx.answers.formula_a)
      ]

    + Find the rate at which the area is changing when $theta = pi\/3$.

      #answer-space(1.6in)
      #if-solution[
        *Answer:* #math-from-str(ctx.answers.value_b)
      ]
  ]
]

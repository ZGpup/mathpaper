// Vertex-form quadratic: transformations from y = x², key features, range.
//
// Context supplies the computed answer values; transformation descriptions
// are assembled in Typst using the numeric parameters from context.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $#math-from-str(ctx.polynomial)$, written in vertex form $a(x-h)^2 + k$.

  #set enum(numbering: "a.")
  + Describe the three transformations applied to $y = x^2$ to produce $f$.
    #parts-grid(numbering: "i.", columns: 1, (
      [
        Horizontal shift #if ctx.h_positive [right] else [left] $#ctx.h_abs$ #if ctx.h_abs == 1 [unit] else [units].
        #answer-space(0.7in)
        #if-solution[
          *Answer:* Replace $x$ with $x - #ctx.h$; shifts graph
          #if ctx.h_positive [right] else [left] $#ctx.h_abs$.
        ]
      ],
      [
        Vertical #if ctx.a_negative [stretch by $#ctx.a_abs$ and reflection over the $x$-axis] else [stretch by a factor of $#ctx.a_abs$].
        #answer-space(0.7in)
        #if-solution[
          *Answer:* Multiply output by $#ctx.a$;
          #if ctx.a_negative [stretches by $#ctx.a_abs$ and flips over $x$-axis.] else [stretches by $#ctx.a_abs$.]
        ]
      ],
      [
        Vertical shift #if ctx.k_positive [up] else [down] $#ctx.k_abs$ units.
        #answer-space(0.7in)
        #if-solution[
          *Answer:* Add $#ctx.k$ to output; shifts graph
          #if ctx.k_positive [up] else [down] $#ctx.k_abs$.
        ]
      ],
    ))

  + Find the following key features of $f$.
    #parts-grid(numbering: "i.", columns: 2, (
      [
        State the vertex.
        #answer-space(0.9in)
        #if-solution[*Answer:* $#math-from-str(ctx.answers.vertex)$]
      ],
      [
        State the axis of symmetry.
        #answer-space(0.9in)
        #if-solution[*Answer:* $#math-from-str(ctx.answers.axis)$]
      ],
      [
        Find the $x$-intercepts algebraically.
        #answer-space(0.9in)
        #if-solution[*Answer:* $#math-from-str(ctx.answers.x_intercepts)$]
      ],
      [
        Find the $y$-intercept.
        #answer-space(0.9in)
        #if-solution[*Answer:* $#math-from-str(ctx.answers.y_intercept)$]
      ],
    ))

  + State the range of $f$ using interval notation.
    #answer-space(0.8in)
    #if-solution[*Answer:* $#math-from-str(ctx.answers.range)$]
]

// Five-part differentiation drill: log rules, log base-b, arcsin, chain rule, quotient with arccos.
//
// ctx.parts is a 5-element array of {expr, answer} dicts. Each expr and answer
// is a Typst math string rendered via math-from-str.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Differentiate each of the following. These derivative rules were derived
  using implicit differentiation. You do not need to simplify your answers.

  #parts-grid(numbering: "a.", columns: 2, (
    [
      $y = #math-from-str(ctx.parts.at(0).expr)$. Find $y'$.
      #answer-space(1.8in)
      #if-solution[*Answer:* $y' = #math-from-str(ctx.parts.at(0).answer)$]
    ],
    [
      $y = #math-from-str(ctx.parts.at(1).expr)$. Find $y'$.
      #answer-space(1.8in)
      #if-solution[*Answer:* $y' = #math-from-str(ctx.parts.at(1).answer)$]
    ],
    [
      $y = #math-from-str(ctx.parts.at(2).expr)$. Find $y'$.
      #answer-space(1.8in)
      #if-solution[*Answer:* $y' = #math-from-str(ctx.parts.at(2).answer)$]
    ],
    [
      $y = #math-from-str(ctx.parts.at(3).expr)$. Find $y'$.
      #answer-space(1.8in)
      #if-solution[*Answer:* $y' = #math-from-str(ctx.parts.at(3).answer)$]
    ],
    [
      $y = #math-from-str(ctx.parts.at(4).expr)$. Find $y'$.
      #answer-space(1.8in)
      #if-solution[*Answer:* $y' = #math-from-str(ctx.parts.at(4).answer)$]
    ],
  ))
]

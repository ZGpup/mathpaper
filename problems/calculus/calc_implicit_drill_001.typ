// Four-part implicit differentiation drill: polynomial, folium, log, trig.
//
// ctx.parts is a 4-element array of {equation, answer} dicts.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  For each implicit curve below, find $(d y)/(d x)$.

  #parts-grid(numbering: "a.", columns: 2, (
    [
      $#math-from-str(ctx.parts.at(0).equation)$
      #answer-space(2in)
      #if-solution[*Answer:* $#math-from-str(ctx.parts.at(0).answer)$]
    ],
    [
      $#math-from-str(ctx.parts.at(1).equation)$
      #answer-space(2in)
      #if-solution[*Answer:* $#math-from-str(ctx.parts.at(1).answer)$]
    ],
    [
      $#math-from-str(ctx.parts.at(2).equation)$
      #answer-space(2in)
      #if-solution[*Answer:* $#math-from-str(ctx.parts.at(2).answer)$]
    ],
    [
      $#math-from-str(ctx.parts.at(3).equation)$
      #answer-space(2in)
      #if-solution[*Answer:* $#math-from-str(ctx.parts.at(3).answer)$]
    ],
  ))
]

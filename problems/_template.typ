// One-line description.
//
// Sibling Python file computes answers and ships them via context.json.

#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Problem stem goes here.

  #set enum(numbering: "a.")
  + Part a question text.
    #answer-space(1.5in)
    #if-solution[*Answer:* #math-from-str(ctx.answers.part_a)]  // math expression

  + Part b question text.
    #answer-space(1.5in)
    #if-solution[*Answer:* #ctx.answers.part_b]  // plain text
]

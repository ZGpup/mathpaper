#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#import "mathpaper.typ": set-solution-mode
#set-solution-mode(false)

#grid(columns: (1fr, 1fr), align: (left, right))[*Templated Problem Demo*][Algebra 2 / Calculus  Version A]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)

#include "problem_001/problem.typ"

#include "problem_002/problem.typ"

#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#grid(columns: (1fr, 1fr), align: (left, right))[*Linear Equations Worksheet*][Algebra 1]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)


*1. (3 pts)* Solve for x:  2x + 5 = 13

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $x = 4$]

*2. (3 pts)* Solve for x:  3(x - 2) = 9

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $x = 5$]

*3. (8 pts)* Consider the equation  y = 2x - 1.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find the slope.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$2$]
],
[
*b.* Find the y-intercept.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$-1$]
],
[
*c.* Graph the equation on the axes below.

#v(1in)
],
[
*d.* Find x when y = 7.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$x = 4$]
]
)

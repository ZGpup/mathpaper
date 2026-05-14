#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#grid(columns: (1fr, 1fr), align: (left, right))[*Polynomial Functions Quiz*][Algebra 2  Version A]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)


*1. (4 pts)* Factor completely: $x^2 - 3 x + 2$

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $(x - 2) (x - 1)$]

*2. (3 pts)* Find all real zeros of $f(x) = x^2 - 3 x + 2$.

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $1, 2$]

*3. (8 pts)* Let $f(x) = x^3 - 2 x^2 - 11 x + 12$. Use algebra to answer the following.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find all real zeros of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$-3, 1, 4$]
],
[
*b.* Find the $y$-intercept.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(0, 12)$]
],
[
*c.* Describe the end behavior of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$f(x) -> -oo " as " x -> -oo, quad f(x) -> +oo " as " x -> +oo$]
],
[
*d.* State the interval(s) where $f(x) \> 0$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(-3, 1) union (4, +oo)$]
]
)

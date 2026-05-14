#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#grid(columns: (1fr, 1fr), align: (left, right))[*Polynomial Functions Quiz*][Algebra 2  Version A]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)


#block(breakable: false)[
*1. (4 pts)* Factor completely: $2 x^2 - 2 x - 12$

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $2 (x - 3) (x + 2)$]
]

#block(breakable: false)[
*2. (8 pts)* Let $f(x) = x^2 + 3 x - 4$. Use algebra to answer the following.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find all real zeros of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$-4, 1$]
],
[
*b.* Find the $y$-intercept.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(0, -4)$]
],
[
*c.* Describe the end behavior of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$f(x) -> +oo " as " x -> plus.minus oo$]
],
[
*d.* State the interval(s) where $f(x) \< 0$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(-4, 1)$]
]
)
]

#block(breakable: false)[
*3. (10 pts)* Let $f(x) = x^3 - 5 x^2 + 2 x + 8$. Use algebra to answer the following.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find all real zeros of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$-1, 2, 4$]
],
[
*b.* Find the $y$-intercept.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(0, 8)$]
],
[
*c.* Describe the end behavior of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$f(x) -> -oo " as " x -> -oo, quad f(x) -> +oo " as " x -> +oo$]
],
[
*d.* State the interval(s) where $f(x) \> 0$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$(-1, 2) union (4, +oo)$]
],
[
*e.* What is the maximum number of turning points $f$ can have?

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$2$]
]
)
]

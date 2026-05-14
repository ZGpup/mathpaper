#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#grid(columns: (1fr, 1fr), align: (left, right))[*Derivatives Quiz*][Calculus  Version A]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)


#block(breakable: false)[
*1. (4 pts)* Let $f(x) = x^4 - 8 x^2 + 7$. Find $f'(x)$.

#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* $f'(x) = 4 x^3 - 16 x$]
]

#block(breakable: false)[
*2. (10 pts)* Let $f(x) = x^4 - 8 x^2 + 7$. Answer each question below.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find $f'(x)$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$4 x^3 - 16 x$]
],
[
*b.* Find $f''(x)$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$4 (3 x^2 - 4)$]
],
[
*c.* Find all critical points of $f$.

#block(fill: luma(230), inset: 4pt, radius: 3pt)[$x = -2, 0, 2$]
],
[
*d.* Classify each critical point as a local min, local max, or neither.

#v(1.2in)
]
)
]

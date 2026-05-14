#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.6em)
#show math.equation: set text(size: 11pt)

#grid(columns: (1fr, 1fr), align: (left, right))[*Derivatives Quiz*][Calculus  Version A]
Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))

#line(length: 100%, stroke: 0.5pt)
#v(0.3em)


#block(breakable: false)[
*1. (4 pts)* Let $f(x) = x^4 - 8 x^2 + 7$.  Find $f'(x)$.

#v(1.2in)
]

#block(breakable: false)[
*2. (10 pts)* Let $f(x) = x^4 - 8 x^2 + 7$. Answer each question below.

#grid(columns: (1fr, 1fr), column-gutter: 1em, row-gutter: 1em,
[
*a.* Find $f'(x)$.

#v(1.2in)
],
[
*b.* Find $f''(x)$.

#v(1.2in)
],
[
*c.* Find all critical points of $f$.

#v(1.2in)
],
[
*d.* Classify each critical point as a local min, local max, or neither.

#v(1.2in)
]
)
]

#block(breakable: false)[
*3. (6 pts)* Given $x^2 + y^2 = 25$, use implicit differentiation to find $(d y)/(d x)$.

#v(2in)
]

#block(breakable: false)[
*4. (8 pts)* Given $y = x^(y^x)$, use implicit differentiation to find $(d y)/(d x)$.

#v(2.5in)
]

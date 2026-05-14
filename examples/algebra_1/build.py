"""Algebra 1 example — basic linear equations worksheet."""
from mathpaper import Test, Problem, MultipartProblem, Part, Text, Math, AnswerSpace, PartsGrid

quiz = Test(title="Linear Equations Worksheet", course="Algebra 1")

quiz.add(Problem(
    prompt=Text("Solve for x:  2x + 5 = 13"),
    answer=Math("x = 4"),
    answer_space="1in",
    points=3,
))

quiz.add(Problem(
    prompt=Text("Solve for x:  3(x - 2) = 9"),
    answer=Math("x = 5"),
    answer_space="1in",
    points=3,
))

quiz.add(MultipartProblem(
    prompt=Text("Consider the equation  y = 2x - 1."),
    parts=[
        Part("Find the slope.", answer=Math("2")),
        Part("Find the y-intercept.", answer=Math("-1")),
        Part("Graph the equation on the axes below."),
        Part("Find x when y = 7.", answer=Math("x = 4")),
    ],
    layout=PartsGrid(columns=2, answer_space="1in"),
    points=8,
))

quiz.build("out/algebra_1")
print("Built to out/algebra_1/")

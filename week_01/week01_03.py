import sys
import math


def solve_quadratic_equation(a, b, c):
    D = (b ** 2) - (4 * a * c)

    x1 = (-b + math.sqrt(D)) / (2 * a)
    x2 = (-b - math.sqrt(D)) / (2 * a)

    return x1, x2


if __name__ == '__main__':
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    for i in (list(map(int, solve_quadratic_equation(a, b, c)))):
        print(i)

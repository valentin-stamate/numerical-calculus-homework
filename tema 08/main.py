import math

K_MAX = 5000
epsilon = 10 ** (-6)


def f1(x):
    return 1.0 / 3.0 * (x ** 3) - 2 * (x ** 2) + 2 * x + 3


def f2(x):
    return x * x + math.sin(x)


def f3(x):
    return (x ** 4) - 6 * (x ** 3) + 13 * (x ** 2) - 12 * x + 4


def derivative_g1_x(f, x, h=10 ** (-6)):
    return (3 * f(x) - 4 * f(x - h) + f(x - 2 * h)) / (2 * h)


def derivative_g2_x(f, x, h=10 ** (-6)):
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)


def second_derivative_x(f, x, h=10 ** (-6)):
    return (-f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)) / (12 * h * h)


def steffensen_solve(f, x_init):
    k = 0
    x = x_init
    while True:
        g_x = derivative_g1_x(f, x)
        g_x_plus_gx = derivative_g1_x(f, x + g_x)
        if abs(g_x_plus_gx - g_x) <= epsilon:
            if second_derivative_x(f, x) > 0:
                return x, f'Numar iteratii: {k}'
        delta_x = (g_x * g_x) / (g_x_plus_gx - g_x)
        x = x - delta_x
        k += 1
        if abs(delta_x) < epsilon or k == K_MAX or abs(delta_x) >= 10 ** 8:
            break
    if abs(delta_x) < epsilon:
        if second_derivative_x(f, x) > 0:
            return x, f'Numar iteratii: {k}'
    return None, f'Numar iteratii: {k}'


def check(x):
    if x != 1:
        return x
    else:
        return ''


def write_solutions(p, solutions):
    f = open('solutions.txt', 'w+')
    f.write('Solutiile polinomului ')
    n = len(p) - 1
    for i in range(len(p) - 1):
        f.write(f'{check(p[i])}x^{n}')
        if p[i + 1] > 0:
            f.write('+')
        n -= 1
    f.write(f'{p[n]} sunt:\n')
    for i in range(len(solutions)):
        f.write(f'x{i + 1} = {solutions[i]}\n')


def in_solutions(solutions, x):
    for solution in solutions:
        if abs(solution[0] - x) < epsilon:
            return True
    return False


def calculate(f, step=1.01):
    x = None
    value = 0
    solutions = []
    for i in range(10):
        solution = steffensen_solve(f, value)
        value += step
        x = solution[0]
        if x is not None and not in_solutions(solutions, x):
            solutions.append(solution)
    print(solutions)


def main():
    calculate(f1)
    calculate(f2)
    calculate(f3)


if __name__ == '__main__':
    main()

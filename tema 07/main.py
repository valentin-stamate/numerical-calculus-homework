import random

import numpy as np

K_MAX = 5000
epsilon = 10 ** (-6)


def polynomial_value_horner_method(p, x):
    n = len(p)
    b = p[0]
    for i in range(1, n):
        b_next = b * x + p[i]
        b = b_next
    return b


def dehghan_solve(p):
    r = (abs(p[0]) + max(p)) / abs(p[0])
    k = 0
    x = random.uniform(-r, r)
    delta_x = 1
    while True:
        if abs(delta_x) < epsilon or k == K_MAX or abs(delta_x) >= 10 ** 8:
            break
        if abs(polynomial_value_horner_method(p, x)) <= epsilon / 10:
            delta_x = 0
        else:
            p_x = polynomial_value_horner_method(p, x)
            p_x_plus_px = polynomial_value_horner_method(p, x + p_x)
            p_x_minus_px = polynomial_value_horner_method(p, x - p_x)
            y_k = x - (2 * (p_x ** 2) / (p_x_plus_px - p_x_minus_px))
            p_y = polynomial_value_horner_method(p, y_k)
            delta_x = (2 * p_x * (p_x + p_y)) / (p_x_plus_px - p_x_minus_px)
        x = x - delta_x
        k += 1
    if abs(delta_x) < epsilon:
        return x
    else:
        return None


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


def main():
    p = np.array([1, -6, 11, -6])
    solution_integers = []
    solutions = []
    for i in range(50):
        x = dehghan_solve(p)
        print(x)
        if x is not None:
            y = round(x)
            if y not in solution_integers:
                solution_integers.append(y)
                solutions.append(x)

    write_solutions(p, solutions)


if __name__ == '__main__':
    main()

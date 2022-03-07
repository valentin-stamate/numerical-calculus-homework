import math

import numpy as np

eps = 10 ** (-8)


def print_matrix(a, label=''):
    n = a.shape[0]

    if label != '':
        print(label)

    if len(a.shape) == 1:
        for i in range(0, n):
            print('%-5f  ' % a[i], end='')
        print("\n")
        return

    m = a.shape[1]

    for i in range(0, n):
        for j in range(0, m):
            print('%2.6f' % a[i, j])
        print("\n")

    print("\n")


def save_matrix(a, x, n):
    with open('log.txt', 'w') as f:
        for i in range(n):
            for j in range(n + 1):
                trim = (int(a[i, j] * 100000)) / 100000
                s = '%-13f' % trim
                f.write(s)
            f.write('\n')

        f.write('\nSolution\n')

        for i in range(n):
            trim = (int(x[i] * 100000)) / 100000
            s = '%-13f' % trim
            f.write(s)


def solve_triangular_matrix(a, n):
    x = np.zeros(n)

    x[n - 1] = a[n - 1, n] / a[n - 1, n - 1]

    for i in range(n - 2, -1, -1):
        s = 0
        for j in range(i + 1, n):
            s += (a[i, j] * x[j])

        x[i] = (a[i, n] - s) / a[i, i]

    return x


def search_pivot(a, col, n):
    index = 0
    m = -9999999

    for i in range(col, n):
        if abs(a[i, col]) > m:
            m = abs(a[i, col])
            index = i

    return index


def swap_lines(a, i, j):
    a[[i, j]] = a[[j, i]]


def gauss_elimination(a, n, a_init, b_init):
    for col in range(0, n - 1):
        pivot = search_pivot(a, col, n)
        if pivot != col:
            swap_lines(a, col, pivot)

        if abs(a[col, col]) < eps:
            print('Division not possible')
            break

        for i in range(col + 1, n):
            factor = - a[i, col] / a[col, col]

            for j in range(0, n + 1):
                a[i, j] += factor * a[col, j]

    col = n - 1
    if abs(a[col, col]) <= eps:
        print("Singular matrix")
    else:
        x = solve_triangular_matrix(a, n)
        return x

    return None


def extend_matrix(a, n):
    i = np.zeros((n, 2 * n))
    for line in range(n):
        i[line, n + line] = 1
    i[0:n, 0:n] = a
    return i


def gauss_elimination_extended(a, n):
    a = extend_matrix(a, n)
    for col in range(0, n - 1):
        pivot = search_pivot(a, col, n)
        if pivot != col:
            swap_lines(a, col, pivot)

        if abs(a[col, col]) < eps:
            print('Division not possible')
            break

        for i in range(col + 1, n):
            factor = - a[i, col] / a[col, col]

            for j in range(0, 2 * n):
                a[i, j] += factor * a[col, j]

    col = n - 1
    if abs(a[col, col]) <= eps:
        print("Singular matrix")
    else:
        inverse_a = np.zeros((n, n))
        for col in range(n):
            a = swap_columns(a, n, n + col)
            x = solve_triangular_matrix(a, n)
            inverse_a[0:n, col] = x
            a = swap_columns(a, n, n + col)

        return inverse_a

    return None


def swap_columns(a, i, j):
    a[:, [i, j]] = a[:, [j, i]]
    return a


def verify(a_init, x, b_init, n):
    b_cal = np.dot(a_init, x)
    x_calc = b_cal - b_init

    s = 0
    for i in range(n):
        s += (x_calc[i] ** 2)

    return math.sqrt(s)


def main():
    a = np.array([
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ], dtype='float32')
    n = 100
    a = np.random.rand(n, n + 1)

    a_init = np.copy(a)
    b_init = a_init[:, -1]

    # Point 1
    a_init = np.delete(a, axis=1, obj=n)
    x_gauss = gauss_elimination(a, n, a_init, b_init)
    # print("X_gauss = ", end='')
    # print(x_gauss)
    # point 2
    print("||A_init * X_gauss - b_init|| = " + str(verify(a_init, x_gauss, b_init, n)))

    # Point 3
    x_bibl = np.linalg.solve(a_init, b_init)
    print("||X_gauss - X_bibl|| = " + str(np.linalg.norm(x_gauss - x_bibl)))

    a_ = np.linalg.inv(a_init).dot(b_init)
    print("||X_gauss - A^(-1)_bibl * b_init|| = " + str(np.linalg.norm(x_gauss - a_)))
    # Point 4

    a = np.copy(a_init)
    gauss_inverse = gauss_elimination_extended(a, n)
    print("||A^(-1)_gauss - A^(-1)_bibl|| = " + str(np.linalg.norm(np.linalg.inv(a_init) - gauss_inverse)))


if __name__ == '__main__':
    main()

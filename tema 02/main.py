import math

import numpy as np
import sys

eps = 10 ** (-8)


def save_log(a, x, n):
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

    print("Solution:")
    for i in range(n):
        print('X%d = %0.2f' % (i, x[i]), end='\t')
    print("\n")

    return x


def search_pivot(a, l, n):
    index = 0
    m = -9999999

    for i in range(l, n):
        if abs(a[i, l]) > m:
            m = abs(a[i, l])
            index = i

    return index


def swap_lines(a, i, j):
    a[[i, j]] = a[[j, i]]


def gauss_elimination(a, n, a_init, b_init):
    for l in range(0, n - 1):
        pivot = search_pivot(a, l, n)
        if pivot != l:
            print("l=", l, '\n')
            print("pv=", pivot, '\n')
            swap_lines(a, l, pivot)

        if abs(a[l, l]) < eps:
            print('Nu se poate face impartirea')
            break

        for i in range(l + 1, n):
            factor = - a[i, l] / a[l, l]

            for j in range(0, n + 1):
                a[i, j] += factor * a[l, j]

    l = n - 1
    if abs(a[l, l]) <= eps:
        print("Matrice singulara")
    else:
        print(a, '\n\n')
        x = solve_triangular_matrix(a, n)
        norm = verify(a_init, x, b_init, n)
        print("The norm is:")
        print(norm)

        return x

    return None

def gauss_elimination_old(a, n):
    x = np.zeros(n)
    for i in range(n):
        if abs(a[i][i]) < eps:
            print('Divide by zero detected!')
            print('Singular matrix')
            break

        for j in range(i + 1, n):
            ratio = a[j][i] / a[i][i]

            for k in range(n + 1):
                a[j][k] = a[j][k] - ratio * a[i][k]

    x[n - 1] = a[n - 1][n] / a[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        x[i] = a[i][n]

        for j in range(i + 1, n):
            x[i] = x[i] - a[i][j] * x[j]

        x[i] = x[i] / a[i][i]

    # np.savetxt('log.txt', a, delimiter=' ')

    save_log(a, x, n)

    print('\nThe solution is: ')
    for i in range(n):
        print('X%d = %0.2f' % (i, x[i]), end='\t')
    print('\n')

    solve_triangular_matrix(a, n)
    return x


def verify(a_init, x, b_init, n):
    b_cal = np.dot(a_init, x)
    print('B Calc\n', b_cal, '\n')
    print('B Init\n', b_init, '\n')

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

    n = 10
    a = np.random.rand(n, n + 1)

    a_init = np.copy(a)
    b_init = a_init[:, -1]

    a_init = np.delete(a, axis=1, obj=n)
    x_gauss = gauss_elimination(a, n, a_init, b_init)

    # Point 3
    x_bibl = np.linalg.solve(a_init, b_init)
    print(np.linalg.norm(x_gauss - x_bibl))

    a_ = np.linalg.inv(a_init).dot(b_init)
    print(np.linalg.norm(x_gauss - a_))


if __name__ == '__main__':
    main()

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
            print('%-8f   ' % a[i, j], end='')
        print()

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


def gauss_elimination(a, n):
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


def construct_matrix_from_comp(a_comp, n):
    a = np.zeros((n, n + 1), dtype='float32')

    a[0, 0] = a_comp[0, 0]
    a[0, 1] = a_comp[0, 1]

    for i in range(1, n):
        if i == n - 1:
            for j in range(0, 3):
                a[i, i - 1 + j] = a_comp[i, j]
            break

        for j in range(0, 4):
            a[i, i - 1 + j] = a_comp[i, j]

    return a


def extract_comp_from_matrix(a, n):
    a_comp = np.zeros((n, 4), dtype='float32')

    a_comp[0, 0] = a[0, 0]
    a_comp[0, 1] = a[0, 1]

    for i in range(1, n):
        for j in range(0, 3):
            a_comp[i, j] = a[i, i - 1 + j]

    return a_comp


def swap(a, index_i, index_j):
    aux = a[index_i[0], index_i[1]]
    a[index_i[0], index_i[1]] = a[index_j[0], index_j[1]]
    a[index_j[0], index_j[1]] = aux


def gauss_tridiagonal(n):
    original = np.random.rand(n, n + 1)
    a_comp = extract_comp_from_matrix(original, n)
    a_init = construct_matrix_from_comp(a_comp, n)
    b_init = a_init[:, -1]
    a_init = np.delete(a_init, axis=1, obj=n)

    # in mod similar ca si in algoritmul clasic vrem sa facem
    # incepand de la lina 2, prima coloana 0

    a = a_comp[0, 0]
    b = a_comp[0, 1]
    c = a_comp[1, 0]

    ratio = - c / a
    a_comp[1, 0] += ratio * a
    a_comp[1, 1] += ratio * b

    for i in range(1, n - 1):
        a = a_comp[i, 1]
        b = a_comp[i, 2]
        d = a_comp[i, 3]
        c = a_comp[i + 1, 0]

        # pivotare
        if c > a:
            swap(a_comp, (i, 1), (i + 1, 0))
            swap(a_comp, (i, 2), (i + 1, 1))
            swap(a_comp, (i, 3), (i + 1, 2))

        a = a_comp[i, 1]
        b = a_comp[i, 2]
        d = a_comp[i, 3]
        c = a_comp[i + 1, 0]

        ratio = - c / a

        a_comp[i + 1, 0] += ratio * a
        a_comp[i + 1, 1] += ratio * b
        a_comp[i + 1, 2] += ratio * d

    a = construct_matrix_from_comp(a_comp, n)

    x = solve_triangular_matrix(a, n)
    x_lib = np.linalg.solve(a_init, b_init)

    print(np.linalg.norm(x - x_lib))


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
    x_gauss = gauss_elimination(a, n)
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

    # Bonus
    print("Bonus")
    gauss_tridiagonal(n)


if __name__ == '__main__':
    main()

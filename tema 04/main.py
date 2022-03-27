import sys

import numpy as np


prec = 16
eps = 10 ** (- prec)

def read_matrix(path):
    with open(path) as f:
        lines = f.readlines()

    n = int(lines[0])
    lines = lines[2:]

    mp = [{} for _ in range(n)]

    for line in lines:
        val, i, j = line.split(',')
        val = float(val.strip())
        i = int(i.strip())
        j = int(j.strip())

        if i == j and abs(val) < eps:
            sys.exit('Null element on main diagonal')

        if mp[i].get(j) is not None:
            mp[i][j] += val
            continue

        mp[i][j] = val

    return n, mp


def read_line_matrix(path, n):
    matrix = np.zeros((n, 1), dtype='float32')

    with open(path) as f:
        lines = f.readlines()

    for i in range(len(lines)):
        matrix[i, 0] = float(lines[i].strip())

    return matrix


def main():
    n_a1, a1 = read_matrix('a_1.txt')
    n_a2, a2 = read_matrix('a_2.txt')
    n_a3, a3 = read_matrix('a_3.txt')
    n_a4, a4 = read_matrix('a_4.txt')
    n_a5, a5 = read_matrix('a_5.txt')

    b1 = read_line_matrix('b_1.txt', n_a1)
    b2 = read_line_matrix('b_2.txt', n_a2)
    b3 = read_line_matrix('b_3.txt', n_a3)
    b4 = read_line_matrix('b_4.txt', n_a4)
    b5 = read_line_matrix('b_5.txt', n_a5)


if __name__ == '__main__':
    main()

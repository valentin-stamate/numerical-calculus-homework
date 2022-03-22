import numpy as np
import time


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

        if mp[i].get(j) is not None:
            mp[i][j] += val
            continue

        mp[i][j] = val

    return n, mp


def to_matrix(a: list[dict], sym=False):
    n = len(a)

    matrix = np.zeros((n, n), dtype='float32')

    for i in range(n):
        for k, value in a[i].items():
            if sym:
                matrix[i, k] = matrix[k, i] = value
                continue

            matrix[i, k] = value

    return matrix


def sum_matrix(a, b):
    start_time = time.time()

    n = len(a)
    r = [{} for _ in range(n)]

    for i in range(n):
        for j, value in a[i].items():
            r[i][j] = value

    for i in range(n):
        for j, value in b[i].items():
            if r[i].get(j) is not None:
                r[i][j] += value
                continue

            r[i][j] = value
    print("---Timp adunare %s seconds ---" % (time.time() - start_time))
    return r


def square_matrix(a: list[dict]):
    start_time = time.time()

    n = len(a)

    prod = [{} for _ in range(n)]

    for i in range(n):
        for j, value in a[i].items():
            a[j][i] = value

    for i in range(n):
        line_a = a[i]
        for j in range(n):
            # numai valorile nenule de pe linia i a se vor inmulti
            # cu valorile nenule de pe linia j
            s = 0
            for k, lin in line_a.items():
                col = a[k].get(j)

                if col is None:
                    col = a[j].get(k)

                if col is not None:
                    s += lin * col

            if s != 0:
                prod[i][j] = s
    print("---Timp inmultire %s seconds ---" % (time.time() - start_time))
    return prod


# sym means the values are only below diagonal, but it's symmetric
def check(a: list[dict], b: list[dict], a_sym=True, b_sym=True):
    n = len(a)

    a_m = to_matrix(a, a_sym)
    b_m = to_matrix(b, b_sym)

    for i in range(n):
        for j in range(n):
            if a_m[i, j] != b_m[i, j]:
                print(f'{a_m[i, j]} vs {b_m[i, j]}')
                return False

    return True


def main():
    n, a = read_matrix('a.txt')
    _, b = read_matrix('b.txt')

    _, a_p_b = read_matrix('a_plus_b.txt')
    _, a_m_a = read_matrix('a_ori_a.txt')

    _sum = sum_matrix(a, b)
    print("Sum is correct?", check(_sum, a_p_b))

    _square = square_matrix(a)
    print("Squared is correct?", check(_square, a_m_a, False, True))


if __name__ == "__main__":
    main()

import math
import random
import numpy as np


def identity_matrix(n) -> np.ndarray:
    a = np.zeros((n, n), dtype='float32')

    for i in range(n):
        a[i, i] = 1

    return a


# A = R_pq(O) * A * R_pq^T(O)
def next_a(a, p, q, c, s, t) -> np.ndarray:
    n = len(a)
    a = np.copy(a)

    for j in range(0, n):
        if j == p or j == q:
            continue
        a[p, j] = c * a[p, j] + s * a[q, j]
        a[q, j] = a[j, q] = -s * a[j, p] + c * a[q, j]
        a[j, p] = a[p, j]

    a[p, p] += t * a[p, q]
    a[q, q] -= t * a[p, q]
    a[p, q] = a[q, p] = 0

    return a


# U = U * R_pq^t(O)
def next_u(u, p, q, c, s, t) -> np.ndarray:
    n = len(u)
    old_u = u
    u = np.copy(u)

    for i in range(n):
        u[i, p] = c * u[i, p] + s * u[i, q]
        u[i, q] = -s * old_u[i, p] + c * u[i, q]

    return u


# c, s, t
def calculate_values(a, p, q):
    alpha = (a[p, p] - a[q, q]) / (2 * a[p, q])

    t = -alpha + np.sign(alpha) * math.sqrt(alpha * alpha + 1)
    c = 1 / math.sqrt(1 + t * t)
    s = t / math.sqrt(1 + t * t)

    return c, s, t


def calculate_pq(a):
    n = len(a)

    p, q = 1, 0
    m = 0

    for i in range(0, n):
        for j in range(0, i):
            if abs(a[i, j]) > m:
                m = abs(a[i, j])
                p, q = i, j

    return m, p, q


def calculate_angle(a, p, q):
    n = len(a)

    c = s = t = 0

    return c, s, t


def generate_symmetric_matrix(n) -> np.ndarray:
    ar = np.zeros((n, n), dtype='float32')

    for i in range(n):
        for j in range(i + 1):
            ar[i, j] = ar[j, i] = random.random() * 10

    return ar


def jacobi_method_for_eigenvalues(a):
    n = len(a)
    eps = 10 ** (-6)

    apq, p, q = calculate_pq(a)
    c, s, t = calculate_values(a, p, q)
    u = identity_matrix(n)

    k = 0
    while apq > eps and k <= 1000:
        a = next_a(a, p, q, c, s, t)
        u = next_u(u, p, q, c, s, t)

        apq, p, q = calculate_pq(a)
        c, s, t = calculate_values(a, p, q)

        k += 1

    # an eigen vector is found in a column
    eigen_vector = np.copy(u)
    eigen_values = np.zeros((1, n), dtype='float32')

    for i in range(n):
        eigen_values[0, i] = a[i, i]

    return eigen_vector, eigen_values


def main():

    a = generate_symmetric_matrix(4)
    eigen_vector, eigen_values = jacobi_method_for_eigenvalues(a)

    print('EigenValues\n', eigen_values)
    print('EigenVectors\n', eigen_vector)

    print('Library')
    library_result = np.linalg.eigh(a)
    print('EigenValues\n', library_result[0])
    print('EigenVectors\n', library_result[1])

if __name__ == '__main__':
    main()

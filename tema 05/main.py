import math
import random
import numpy as np
import matplotlib.pyplot as plt

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


def generate_symmetric_matrix(n) -> np.ndarray:
    ar = np.zeros((n, n), dtype='float32')

    for i in range(n):
        for j in range(i + 1):
            ar[i, j] = ar[j, i] = random.random() * 10

    return ar


def extract_eigenvector(u) -> np.ndarray:
    return np.copy(u)


def extract_eigenvalues(a) -> np.ndarray:
    n = len(a)
    eigen_values = np.zeros((1, n), dtype='float32')

    for i in range(n):
        eigen_values[0, i] = a[i, i]

    return eigen_values


def jacobi_method_for_eigenvalues(a):
    n = len(a)
    eps = 10 ** (-6)

    a_old = a.copy()

    apq, p, q = calculate_pq(a)
    c, s, t = calculate_values(a, p, q)
    u = identity_matrix(n)

    evolution = []

    k = 0
    while apq > eps and k <= 1000:
        a = next_a(a, p, q, c, s, t)
        u = next_u(u, p, q, c, s, t)

        apq, p, q = calculate_pq(a)
        c, s, t = calculate_values(a, p, q)

        # for plot
        eigen_vector = extract_eigenvector(u)
        eigen_values = extract_eigenvalues(a)

        evolution.append(check_jacobi(a_old, eigen_vector, eigen_values))

        k += 1

    # an eigen vector is found in a column
    eigen_vector = extract_eigenvector(u)
    eigen_values = extract_eigenvalues(a)

    return eigen_values, eigen_vector, evolution


def check_jacobi(a, u, lamb):
    return np.linalg.norm(a.dot(u) - u * lamb)


def main():
    n = 25

    a = generate_symmetric_matrix(n)
    lamb, u, evolution = jacobi_method_for_eigenvalues(a)

    # Exercise 1
    print(check_jacobi(a, u, lamb))
    plt.plot(evolution)
    plt.title(f'Evolution, n={n}')
    plt.xlabel('Iteration')
    plt.ylabel('||AU - Uλ||')
    plt.show()

    # Exercise 2
    # print('Computed')
    # print('EigenValues\n', lamb)
    # print('EigenVectors\n', u)

    # lamb_lib, u_lib = np.linalg.eigh(a)
    # print('Library')
    # print('EigenValues\n', lamb_lib)
    # print('EigenVectors\n', u_lib)

    lamb_lib, u_lib = np.linalg.eigh(a)
    print(np.min(lamb - lamb_lib))


if __name__ == '__main__':
    main()

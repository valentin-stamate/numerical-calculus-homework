import numpy as np


class LeastSquaresInterpolation:
    def __init__(self, m):
        self.m = m
        self.coeff = []

    def create_polynom(self, x, y):
        self.coeff = []

        B = np.zeros((self.m + 1, self.m + 1), dtype='float32')

        m = self.m
        n = len(x) - 1

        # Construct B
        for i in range(m + 1):
            for j in range(m + 1):
                su = 0

                for k in range(n + 1):
                    su += (x[k] ** (i + j))

                B[i, j] = su

        # Construct F
        f = np.zeros((1, m + 1), dtype='float32')

        for i in range(m + 1):

            su = 0
            for k in range(n + 1):
                su += (y[k] * (x[k] ** i))

            f[0, i] = su

        # Compute alpha
        alpha = np.linalg.solve(B, f.transpose())
        alpha = np.array(alpha).transpose()

        self.coeff = [val for val in alpha[0]]
        # F = a0 + a1 * x + a2 * x^2 .... + am * x^m

    def fun(self, x):
        d = self.coeff[0]

        for i in range(1, self.m + 1):
            d = self.coeff[i] + d * x

        return d

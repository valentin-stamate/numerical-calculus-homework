
class LagrangePolynom:

    def __init__(self):
        self.coeff = []
        self.x = []
        self.y = []

    def create_polynom(self, x, y):
        self.x = []
        self.y = []
        self.coeff = []

        n = len(x) - 1

        for i in range(len(x)):
            self.x.append(x[i])
            self.y.append(y[i])

        self.coeff.append(y[0])

        # Calculating the coefficients
        for k in range(2, n + 1):
            su = 0

            for i in range(k):
                pr = 1

                for j in range(k):
                    if i == j:
                        continue

                    pr *= x[i] - x[j]

                if pr == 0:
                    pr = 10 ** (-12)

                su += y[i] / pr

            self.coeff.append(su)

    def fun(self, x):
        su = 0

        su += self.coeff[0]

        for i in range(1, len(self.coeff)):

            pr = 1
            for k in range(i):
                pr *= (x - self.x[k])

            su += self.coeff[i] * pr

        return su

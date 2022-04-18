import math
import random
import matplotlib.pyplot as plt
from lagrange import LagrangePolynom
from leastsquares import LeastSquaresInterpolation


def f(x):
    # return x ** 2 - 12 * x + 30 # [1, 5]
    return math.sin(x) - math.cos(x) # [0, 4.75]
    # return 2 * (x ** 3) - 3 * x + 15 # [0, 2]


def show_plot(x, y, x_calc, y_calc, calc_label):
    line1, = plt.plot(x, y, label='real')
    line2, = plt.plot(x_calc, y_calc, label=calc_label)
    plt.legend(handles=[line1, line2])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def get_error(x, fun_appr):
    su = 0
    for i in range(len(x)):
        x_fun = f(x[i])
        x_calc = fun_appr.fun(x[i])

        su += abs(x_calc - x_fun)

    return su


def main():
    n = 30
    eps = 10 ** (-1)

    x0 = 0
    xn = 4.75

    x = [round(random.uniform(x0 + eps, xn - eps), 2) for _ in range(1, n)] + [x0, xn]
    x.sort()

    y = []
    for i in range(len(x)):
        y.append(f(x[i]))

    # Exercise 1
    lag = LagrangePolynom()
    lag.create_polynom(x, y)

    x_calc = [round(random.uniform(x0 + eps, xn - eps), 2) for _ in range(1, 100)] + [x0, xn]
    x_calc.sort()

    y_calc = [lag.fun(val) for val in x_calc]

    x_full = x + x_calc
    show_plot(x, y, x_calc, y_calc, 'newton form')

    print('Newton Form Difference:\n', get_error(x_full, lag))

    # Exercise 2
    m = 5
    leastsq = LeastSquaresInterpolation(m)
    leastsq.create_polynom(x, y)

    y_calc = []

    for i in range(len(x)):
        y_calc.append(leastsq.fun(x[i]))

    show_plot(x, y, x, y_calc, 'lest square')
    print('Least Square Difference:\n', get_error(x_full, leastsq))


if __name__ == '__main__':
    main()

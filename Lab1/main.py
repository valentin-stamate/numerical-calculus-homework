import math
import random
import numpy

sinus_alphas = [
    numpy.float32(1805490264.690988571178600370234394843221),
    numpy.float32(-164384678.227499837726129612587952660511),
    numpy.float32(3664210.647581261810227924465160827365),
    numpy.float32(-28904.140246461781357223741935980097),
    numpy.float32(76.568981088717405810132543523682)
]
sinus_bethas = [
    numpy.float32(2298821602.638922662086487520330827251172),
    numpy.float32(27037050.118894436776624866648235591988),
    numpy.float32(155791.388546947693206469423979505671),
    numpy.float32(540.567501261284024767779280700089),
    numpy.float32(1.0)
]
cosinus_alphas = [
    numpy.float32(1090157078.174871420428849017262549038606),
    numpy.float32(-321324810.993150712401352959397648541681),
    numpy.float32(12787876.849523878944051885325593878177),
    numpy.float32(-150026.206045948110568310887166405972),
    numpy.float32(538.333564203182661664319151379451)
]
cosinus_bethas = [
    numpy.float32(1090157078.174871420428867295670039506886),
    numpy.float32(14907035.776643879767410969509628406502),
    numpy.float32(101855.811943661368302608146695082218),
    numpy.float32(429.772865107391823245671264489311),
    numpy.float32(1.0)
]
logarithm_alphas = [
    numpy.float32(75.151856149910794642732375452928),
    numpy.float32(-134.730399688659339844586721162914),
    numpy.float32(74.201101420634257326499008275515),
    numpy.float32(-12.777143401490740103758406454323),
    numpy.float32(0.332579601824389206151063529971)
]
logarithm_bethas = [
    numpy.float32(37.575928074955397321366156007781),
    numpy.float32(-79.890509202648135695909995521310),
    numpy.float32(56.215534829542094277143417404711),
    numpy.float32(-14.516971195056682948719125661717),
    numpy.float32(1.0)
]


def generate_numbers():
    return random.random(), random.random(), random.random()


def p4(x, coef):
    return coef[0] + x * (coef[1] + x * (coef[2] + x * (coef[3] + x * coef[4])))


def ex1():
    m = 1
    u = pow(10, -m)
    while 1.0 + u != 1.0:
        m += 1
        u = pow(10, -m)
    return u * 10


def ex2():
    ex2_check_addition()
    ex2_check_multiply()


def ex2_check_addition():
    count = 0
    while True:
        count += 1
        a, b, c = generate_numbers()
        if (a + b) + c != a + (b + c):
            print(f"Found in {count} iterations")
            print(f"Values: {a} {b} {c}")
            return count


def ex2_check_multiply():
    count = 0
    while True:
        count += 1
        a, b, c = generate_numbers()
        if (a * b) * c != a * (b * c):
            print(f"Found in {count} iterations")
            print(f"Values: {a} {b} {c}")
            return count


def approximate_sinus(x):
    if not -1 <= x <= 1:
        print("x must be in [-1,1]")
        return None
    return x * p4(x * x, sinus_alphas) / p4(x * x, sinus_bethas)


def approximate_cosinus(x):
    if not -1 <= x <= 1:
        print("x must be in [-1,1]")
        return None
    return p4(x * x, cosinus_alphas) / p4(x * x, cosinus_bethas)


def approximate_logarithm(x):
    if not -1 <= x <= 1:
        print("x must be in [-1/sqrt(2),sqrt(2)]")
        return None
    z = (x - 1) / (x + 1)
    return z * p4(z * z, logarithm_alphas) / p4(z * z, logarithm_bethas)


def ex3():
    x = 0.5
    sin = approximate_sinus(x)
    actual_sin = math.sin(math.pi * x / 4)
    cos = approximate_cosinus(x)
    actual_cos = math.cos(math.pi * x / 4)
    ln = approximate_logarithm(x)
    actual_ln = math.log(x)
    print("Sinus value : " + str(sin))
    print("Actual Value : " + str(actual_sin))
    print("Error : " + str(abs(sin - actual_sin)))
    print("Cosinus value :" + str(cos))
    print("Actual Value : " + str(actual_cos))
    print("Error : " + str(abs(cos - actual_cos)))
    print("Logarithm value :" + str(ln))
    print("Actual Value : " + str(actual_ln))
    print("Error : " + str(abs(ln - actual_ln)))


def main():
    print(ex1())
    ex2()
    ex3()


if __name__ == '__main__':
    main()

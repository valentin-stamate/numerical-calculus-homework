import math
import random
import numpy
import matplotlib.pyplot as plt
import tkinter as tk

from PIL import Image

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
    u = ex1()
    a, b, c = (1.0, u / 10, u / 10)
    if (a + b) + c != a + (b + c):
        return f"Addition is not associative for values: \n{a}\n{b}\n{c}"


def ex2_check_multiply():
    count = 0
    while True:
        count += 1
        a, b, c = generate_numbers()
        if (a * b) * c != a * (b * c):
            return f"Multiplication is not associative for values: \n {a}\n{b}\n{c} \n (Found in {count} iterations)"


def approximate_sinus(x):
    if not -1 <= x <= 1:
        print("x must be in [-1,1] vs %f" % x)
        return None
    return x * p4(x * x, sinus_alphas) / p4(x * x, sinus_bethas)


# using sin(2x) formula
# this function can accept values between [-pi/2, pi/2]
def sin_extended(x):
    return 2 * approximate_sinus(x / 2) * approximate_cosinus(x / 2)


# using cos(2x) formula
# this function can accept values between [-pi/2, pi/2]
def cos_extended(x):
    return approximate_cosinus(x / 2) ** 2 - approximate_sinus(x / 2) ** 2


def reduce_sin_quadrant(x):
    x = x % (2 * math.pi)

    # second quadrant
    if math.pi / 2 <= x < math.pi:
        x = math.pi - x

    # third quadrant
    if math.pi <= x < 3 * math.pi / 2:
        x = - (x - math.pi)

    # forth quadrant
    if 3 * math.pi / 2 <= x <= 2 * math.pi:
        x = - (2 * math.pi - x)

    return x


# reduce the angle to first quadrant and calculates the sin value
def approximate_sinus_general(x):
    # using sin(-x) = -sin(x)
    x = reduce_sin_quadrant(x)
    return sin_extended(x)


# reduce the angle to first quadrant and calculates the sin value
def approximate_cosin_general(x):
    # using cos(x -+ pi/2) = -+sin(x)
    x = reduce_sin_quadrant(x + math.pi / 2)
    return sin_extended(x)


def approximate_cosinus(x):
    if not -1 <= x <= 1:
        print("x must be in [-1,1]")
        return None
    return p4(x * x, cosinus_alphas) / p4(x * x, cosinus_bethas)


def approximate_logarithm(x):
    if not 1 / math.sqrt(2) <= x <= math.sqrt(2):
        print("x must be in [1/sqrt(2),sqrt(2)]")
        return None
    z = (x - 1) / (x + 1)
    return z * p4(z * z, logarithm_alphas) / p4(z * z, logarithm_bethas)


def angle_to_radians(angle):
    return (angle * math.pi) / 180.0


def ex3(x):
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


# BONUS
def bonus():
    x = []
    y = []
    z = []
    plt.close('all')
    for angle in range(-720, 720):
        rad = angle_to_radians(angle)

        x.append(rad)
        y.append(approximate_sinus_general(rad))
        z.append(math.sin(rad))
    plt.plot(x, y)
    plt.plot(x, z)
    plt.ylabel('sin(x)')
    plt.title('Sinus')
    plt.legend(['Aprox value', 'Actual value'], loc='upper right')
    plt.savefig('sin.png', format='png')
    plt.close()

    x = []
    y = []
    z = []
    for angle in range(-720, 720):
        rad = angle_to_radians(angle)

        x.append(rad)
        y.append(approximate_cosin_general(rad))
        z.append(math.cos(rad))
    plt.plot(x, y)
    plt.plot(x, z)
    plt.ylabel('cos(x)')
    plt.title('Cosinus')
    plt.legend(['Aprox value', 'Actual value'], loc='lower right')
    plt.savefig('cos.png', format='png')


# #### UI ####
class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Homework 1')
        self.window.resizable(False, False)
        self.window.geometry('800x600')
        self.window.configure(bg='#E3F6FF')
        self.buttons_frame = tk.Frame()
        self.buttons_frame.pack(side='left')
        self.ex1_button = tk.Button(self.buttons_frame, text='Exercise 1', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10, width=15,
                                    command=self.ex1_ui)
        self.ex1_button.grid(row=0, column=0, padx=10, pady=10)
        self.ex2_button = tk.Button(self.buttons_frame, text='Exercise 2', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10, width=15,
                                    command=self.ex2_ui)
        self.ex2_button.grid(row=2, column=0, padx=10, pady=10)
        self.ex3_button = tk.Button(self.buttons_frame, text='Exercise 3', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10, width=15,
                                    command=self.ex3_ui)
        self.ex3_button.grid(row=4, column=0, padx=10, pady=10)
        self.ex_bonus_button = tk.Button(self.buttons_frame, text='Exercise Bonus', activebackground='#4B93B7',
                                         bg='#64CBFF', padx=10, pady=10, width=15,
                                         command=self.ex_bonus_ui)
        self.ex_bonus_button.grid(row=6, column=0, padx=10, pady=10)
        self.content_frame = None
        self.window.mainloop()

    def ex1_ui(self):
        self.destroy_content_frame()
        self.content_frame = tk.Frame(pady=10)
        self.content_frame.pack(side='left')
        tk.Label(self.content_frame,
                 text="Sa se gaseasca cel mai mic numar pozitiv u > 0, de forma u = 10^(−m)(sau u = 2^(−p)),\n "
                      "astfel ca: 1.0 + u != 1.0").grid(row=0)
        tk.Button(self.content_frame, text='Solve', padx=10, pady=10, command=self.solve_ex1).grid(row=1, column=0)

    def ex2_ui(self):
        self.destroy_content_frame()
        self.content_frame = tk.Frame(pady=10)
        self.content_frame.pack(side='left')
        tk.Button(self.content_frame, text='Check Addition Operation', padx=10, pady=10,
                  command=self.solve_ex2_add).grid(
            row=0, column=0)
        tk.Button(self.content_frame, text='Check Multiplication Operation', padx=10, pady=10,
                  command=self.solve_ex2_mult).grid(row=2, column=0)

    def ex3_ui(self):
        self.destroy_content_frame()
        self.content_frame = tk.Frame(pady=10)
        self.content_frame.pack(side='left')
        self.sin_cos_value_entry = tk.Entry(self.content_frame)
        tk.Label(self.content_frame, text='sin/cos argument:', width=15).grid(row=0, column=0)
        tk.Label(self.content_frame, text='ln argument:', width=15).grid(row=1, column=0)
        self.ln_value_entry = tk.Entry(self.content_frame)
        self.sin_cos_value_entry.grid(row=0, column=1)
        self.ln_value_entry.grid(row=1, column=1)
        tk.Button(self.content_frame, text='Solve', padx=10, pady=10, command=self.solve_ex3).grid(row=0, column=2)

    def ex_bonus_ui(self):
        self.destroy_content_frame()
        self.content_frame = tk.Frame(pady=10)
        self.content_frame.pack(side='left')
        tk.Label(self.content_frame, text='sin/cos argument (angle):', width=20).grid(row=0, column=0)
        self.sin_cos_value_entry = tk.Entry(self.content_frame)
        self.sin_cos_value_entry.grid(row=0, column=1)
        tk.Button(self.content_frame, text='Solve', padx=10, pady=10, command=self.solve_bonus).grid(row=0, column=2)
        tk.Button(self.content_frame, text='Sin Graph', padx=10, pady=10,
                  command=lambda: self.show_graph('sin.png')).grid(row=0, column=3)
        tk.Button(self.content_frame, text='Cos Graph', padx=10, pady=10,
                  command=lambda: self.show_graph('cos.png')).grid(row=0, column=4)

    def destroy_content_frame(self):
        try:
            self.content_frame.destroy()
        except AttributeError as _:
            pass

    def solve_ex1(self):
        self.ex1_solution = tk.Listbox(self.content_frame, height=2, width=8)
        self.ex1_solution.grid(row=1, column=1)
        self.ex1_solution.insert(0, ex1())

    def solve_ex2_add(self):
        self.ex2_add_solution = tk.Label(self.content_frame, height=12, width=40)
        self.ex2_add_solution.grid(row=0, column=2)
        self.ex2_add_solution['text'] = ex2_check_addition()

    def solve_ex2_mult(self):
        self.ex2_mult_solution = tk.Label(self.content_frame, height=12, width=40)
        self.ex2_mult_solution.grid(row=2, column=2)
        self.ex2_mult_solution['text'] = ex2_check_multiply()

    def solve_ex3(self):
        self.sin_value = tk.Label(self.content_frame, width=30)
        self.actual_sin_value = tk.Label(self.content_frame, width=30)
        self.cos_value = tk.Label(self.content_frame, width=30)
        self.actual_cos_value = tk.Label(self.content_frame, width=30)
        self.ln_value = tk.Label(self.content_frame, width=30)
        self.actual_ln_value = tk.Label(self.content_frame, width=30)
        self.sin_value.grid(row=2, column=0)
        self.actual_sin_value.grid(row=2, column=1)
        self.cos_value.grid(row=3, column=0)
        self.actual_cos_value.grid(row=3, column=1)
        self.ln_value.grid(row=4, column=0)
        self.actual_ln_value.grid(row=4, column=1)
        x = float(self.sin_cos_value_entry.get())
        self.sin_value['text'] = 'Aprox sin value ' + str(approximate_sinus(x))
        self.actual_sin_value['text'] = 'Actual sin value ' + str(math.sin(math.pi * x / 4))
        self.cos_value['text'] = 'Aprox cos value ' + str(approximate_cosinus(x))
        self.actual_cos_value['text'] = 'Actual cos value ' + str(math.cos(math.pi * x / 4))
        x = float(self.ln_value_entry.get())
        self.ln_value['text'] = 'Aprox ln value ' + str(approximate_logarithm(x))
        self.actual_ln_value['text'] = 'Actual ln value ' + str(math.log(x))

    def solve_bonus(self):
        self.sin_value = tk.Label(self.content_frame, width=30)
        self.actual_sin_value = tk.Label(self.content_frame, width=30)
        self.cos_value = tk.Label(self.content_frame, width=30)
        self.actual_cos_value = tk.Label(self.content_frame, width=30)
        self.sin_value.grid(row=2, column=0)
        self.actual_sin_value.grid(row=2, column=1)
        self.cos_value.grid(row=3, column=0)
        self.actual_cos_value.grid(row=3, column=1)
        x = float(self.sin_cos_value_entry.get())
        self.sin_value['text'] = 'Aprox sin value ' + str(approximate_sinus_general(angle_to_radians(x)))
        self.actual_sin_value['text'] = 'Actual sin value ' + str(math.sin(angle_to_radians(x)))
        self.cos_value['text'] = 'Aprox cos value ' + str(approximate_cosin_general(angle_to_radians(x)))
        self.actual_cos_value['text'] = 'Actual cos value ' + str(math.cos(angle_to_radians(x)))

    def show_graph(self, file):
        print(file)
        Image.open(file).show()


def main():
    # print(ex1())
    # ex2()
    # ex3()
    UI()
    # bonus()


if __name__ == '__main__':
    main()

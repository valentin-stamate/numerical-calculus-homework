

def read_matrix(path):
    with open(path) as f:
        lines = f.readlines()

    n = int(lines[0])
    lines = lines[2:]

    mp = {}

    for line in lines:
        val, i, j = line.split(',')
        val = float(val.strip())
        i = int(i.strip())
        j = int(j.strip())

        key = (i, j)

        if mp.get(key) is not None:
            mp[key] += val
            continue

        mp[key] = val

    return n, mp


def sum_matrix(a, b):
    r = {}

    for key, value in a.items():
        r[key] = value

    for key, value in b.items():

        if r.get(key) is not None:
            r[key] += value
            continue

        r[key] = value

    return r


def multiply_matrix(a, b, n):

    prod = {}

    for i in range(n):
        print(i)
        for j in range(n):
            s = 0
            for k in range(n):
                x = a.get((i, k))
                if x is None:
                    x = a.get((k, i))

                y = b.get((k, j))
                if y is None:
                    y = b.get((j, k))

                if x is not None and y is not None:
                    s += x * y

            if s != 0:
                prod[(i, j)] = s

    return prod


def check(a, b):
    a_items = a.items()
    b_items = b.items()

    if len(a_items) != len(b_items):
        return False

    for key, value in a_items:
        if b.get(key) != value:
            return False

    return True


def main():
    n, a = read_matrix('a.txt')
    _, b = read_matrix('b.txt')

    _, a_p_b = read_matrix('a_plus_b.txt')
    _, a_m_a = read_matrix('a_ori_a.txt')

    _sum = sum_matrix(a, b)
    print("Sum is correct?", check(_sum, a_p_b))

    print()

    _prod = multiply_matrix(a, a, n)
    print("Product is correct?", check(_prod, a_m_a))


if __name__ == "__main__":
    main()
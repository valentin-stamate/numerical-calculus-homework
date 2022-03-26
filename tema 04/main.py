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


def main():
    n, a1 = read_matrix('a_1.txt')
    _, a2 = read_matrix('a_1.txt')
    _, a3 = read_matrix('a_1.txt')
    _, a4 = read_matrix('a_1.txt')
    _, a5 = read_matrix('a_1.txt')

    print(n)


if __name__ == '__main__':
    main()

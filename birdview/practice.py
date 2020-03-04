def print_star_tree(n):
    for i in range(1, n + 1):
        if i <= (n + 1) // 2:
            print((' ' * (-i + ((n + 1) // 2))) + ('*' * ((2 * i) - 1)))
        elif i > (n + 1) // 2:
            print((' ' * (i - ((n + 1) // 2))) + ('*' * (((2 * n) + 1) - (2 * i))))


def print_triangle(n):
    for i in range(1, n + 1):
        print(' ' * (n + 1 - i) + '*' * i)


def print_multiplication_table(n):
    for i in range(1, 10):
        print('{} * {} = {}'.format(n, i, n*i))


def print_star_tree_2(n):
    half = int(n / 2)
    a = half
    for i in range(1, half):
        print(' ' * a + '*' * (2 * i - 1))
        a -= 1
    for i in range(half + 1, n):
        print(' ' * a + '*' * (2 * (n-i) - 1))
        a += 1


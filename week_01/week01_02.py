import sys


def draw_stairs(num: int):
    for i in range(1, num + 1):
        print((' ' * (num - i) + '#' * i))


if __name__ == '__main__':
    number = sys.argv[1]

    draw_stairs(int(number))

import sys


def calculate_sum_of_digits(digits: str) -> int:
    _sum = 0

    for digit in digits:
        _sum += int(digit)

    return _sum


if __name__ == '__main__':
    digit_string = sys.argv[1]

    print(calculate_sum_of_digits(digit_string))

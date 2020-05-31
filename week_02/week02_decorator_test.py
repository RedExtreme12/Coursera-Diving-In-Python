import functools
import numpy as np

# Логирование результата решения СЛАУ.


A = np.array([[1, 4, 8],
             [1, 2, 6],
             [4, 7, 10]])
b = np.array([1, 2, 3])


def logger(filename):
    def decorator(func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            np.savetxt(filename, result, header='Result of solve: ')

            return result
        return wrapped
    return decorator


@logger('result_solve_systems.txt')
def solve_system_lq(matrix, b):
    return np.linalg.solve(matrix, b)


if __name__ == '__main__':
    print(solve_system_lq(A, b))

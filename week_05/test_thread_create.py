from multiprocessing import Process
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed


class PrintProcess(Process):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')


numbers = [1, 20, 400, 500, 2000, 4]


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        result = zip(numbers, executor.map(lambda x: x ** 2, numbers))
        for number, square_number in result:
            print(f'{number}: {square_number}')

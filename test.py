from datetime import datetime
import time


class SuperCar:

    def __init__(self, __name):
        self.name = __name

    def __getattr__(self, item):
        return 'Nothing found, sorry :(\n'

    def __getattribute__(self, item):
        print(f'Looking for {item}')
        return object.__getattribute__(self, item)


class MyClass:
    def __init__(self, __value):
        self.value = __value

    def __call__(self, *args, **kwargs):
        print(kwargs['hello'])


class TimeManager:

    def __init__(self):
        pass

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *args):
        time.sleep(2.5)
        self.end = datetime.now() - self.start
        print(self.end)


def test_MyClass_SuperCar():
    Tesla = SuperCar('Model Y')
    # print(Tesla.name)
    # print(Tesla.fuck)

    a = MyClass('hello')
    a(**{'hello': 'hi'})


class Value:

    def __init__(self):
        self.value = None

    @staticmethod
    def pow_mod_2(value):
        return pow(value, 1, 2)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = self.pow_mod_2(value)


class TestClassDescriptor:
    attr = Value()


if __name__ == '__main__':
    # test_MyClass_SuperCar()
    # with TimeManager():
    #     print('Hello, I am here!')
    instance = TestClassDescriptor()
    instance.attr = 9
    print(instance.attr)

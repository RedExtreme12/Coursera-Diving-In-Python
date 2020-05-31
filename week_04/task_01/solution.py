import os.path
import tempfile


class File:

    __WRITE_MODE__ = 'w'

    def __init__(self, __path):
        self.path = __path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def __str__(self):
        return os.path.realpath(self.path)

    def __add__(self, other_obj):
        temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        new_obj = File(temp.name)

        new_content = self.read() + other_obj.read()  # Обработка исключения AttributeError
        new_obj.write(new_content)

        return new_obj

    def __iter__(self):
        return self

    def __next__(self):
        line = self.read_line()

        if not line:
            raise StopIteration

        return line

    def read_line(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)
            result = f.readline().rstrip('\n')
            self.current_position = f.tell()

            return result

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, content):
        with open(self.path, self.__WRITE_MODE__) as f:
            result = f.write(str(content))
            self.current_position = f.seek(0)

            return result

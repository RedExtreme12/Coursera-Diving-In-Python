import os.path
import csv


class CarBase:
    _photo_extensions = ('.jpg', '.jpeg', '.png', '.gif')

    index_car_type = 0
    index_brand = 1
    index_passenger_seats_count = 2
    index_photo_file_name = 3
    index_body_whl = 4
    index_carrying = 5
    index_extra = 6

    def __init__(self, __brand, __photo_file_name, carrying):
        self.photo_file_name = __photo_file_name
        self.brand = __brand
        self.carrying = float(carrying)

    @staticmethod
    def _get_photo_file_ext(value):
        return os.path.splitext(value)[1]

    def get_photo_file_ext(self):
        extension = self._get_photo_file_ext(self.photo_file_name)

        if extension in self._photo_extensions:
            return extension
        else:
            return ''

    @property
    def photo_file_name(self):
        return self._photo_file_name

    @photo_file_name.setter
    def photo_file_name(self, value):
        if self._get_photo_file_ext(value) in self._photo_extensions:
            self._photo_file_name = value
        else:
            raise ValueError('Incorrect extension')

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        if value:
            self._brand = value
        else:
            raise ValueError('Incorrect Brand')


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.passenger_seats_count = int(passenger_seats_count)
        super().__init__(brand, photo_file_name, carrying)

    @classmethod
    def create_from_csv(cls, row):
        obj = cls(row[CarBase.index_brand],
                  row[CarBase.index_photo_file_name],
                  row[CarBase.index_carrying],
                  row[CarBase.index_passenger_seats_count], )
        return obj


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)

        try:
            length, width, height = list(map(float, body_whl.split('x')))
        except ValueError:
            length, width, height = 0., 0., 0.

        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    @classmethod
    def create_from_csv(cls, row):
        obj = cls(row[CarBase.index_brand],
                  row[CarBase.index_photo_file_name],
                  row[CarBase.index_carrying],
                  row[CarBase.index_body_whl], )
        return obj


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, __extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = __extra

    @classmethod
    def create_from_csv(cls, row):
        obj = cls(row[CarBase.index_brand],
                  row[CarBase.index_photo_file_name],
                  row[CarBase.index_carrying],
                  row[CarBase.index_extra], )
        return obj

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, value):
        if value:
            self._extra = value
        else:
            raise ValueError('Incorrect Brand')


def get_car_list(csv_file_name):
    with open(csv_file_name, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')

        try:
            next(reader)
        except StopIteration:
            pass

        car_list = []

        for row in reader:
            try:
                car_type = row[0]
            except IndexError:
                continue

            if car_type == Car.car_type or car_type == Truck.car_type:
                row.pop()

            try:
                if car_type == Car.car_type and len(row) == 6:
                    car_list.append(Car.create_from_csv(row))
                elif car_type == Truck.car_type and len(row) == 6:
                    car_list.append(Truck.create_from_csv(row))
                elif car_type == SpecMachine.car_type and len(row) == 7:
                    car_list.append(SpecMachine.create_from_csv(row))
            except (ValueError, IndexError):
                continue

        return car_list


if __name__ == '__main__':
    cars = get_car_list('cars.csv')

    for car in cars:
        print(type(car))

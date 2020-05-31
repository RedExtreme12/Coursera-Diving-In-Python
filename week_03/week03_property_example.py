class AlcoholicDrink:

    def __init__(self, degrees):
        self._degrees = degrees

    degrees = property()

    @degrees.setter
    def degrees(self, value):
        if value < 0:
            self._degrees = 0
        elif value > 50:
            self._degrees = 50
        else:
            self._degrees = value

    @degrees.getter
    def degrees(self):
        return self._degrees


if __name__ == '__main__':
    drink = AlcoholicDrink(20)
    print(drink.degrees)
    drink.degrees = -10
    print(drink.degrees)

class Direction:
    def __init__(self, x, y):
        if type(x) is int and type(y) is int:
            self.x = x
            self.y = y
        else:
            raise ValueError("Invalid argument, expected integer coordinate values, got %s and %s".format(type(x),
                                                                                                          type(y)))

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, amount):
        self.__x = amount

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, amount):
        self.__y = amount

    def __add__(self, other):
        if type(other) is Coordinate:
            Coordinate(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Invalid argument, expected Coordinate, got %s".format(type(other)))


class Coordinate(Direction):
    def __init__(self, x, y):
        super(Coordinate, self).__init__(x, y)


class Up(Direction):
    def __init__(self):
        super(Up, self).__init__(0, -1)


class Down(Direction):
    def __init__(self):
        super(Down, self).__init__(0, 1)


class Left(Direction):
    def __init__(self):
        super(Left, self).__init__(-1, 0)


class Right(Direction):
    def __init__(self):
        super(Right, self).__init__(1, 0)


class Stop(Direction):
    def __init__(self):
        super(Stop, self).__init__(0, 0)
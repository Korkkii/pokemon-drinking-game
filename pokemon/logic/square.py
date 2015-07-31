from abc import abstractmethod, ABCMeta


class Square:
    def __init__(self, desc, number):
        self.__description = desc
        self.__number = number

    @property
    def description(self):
        return self.__description

    @property
    def number(self):
        return self.__number

    @abstractmethod
    def perform_action(self, player):
        raise NotImplementedError

    def __eq__(self, other):
        return self.number == other.number and type(self) is type(other)


class GymSquare(Square, metaclass=ABCMeta):
    def __init__(self, desc, number):
        super(GymSquare, self).__init__(desc, number)


class SpecialSquare(Square, metaclass=ABCMeta):
    def __init__(self, desc, number):
        super(SpecialSquare, self).__init__(desc, number)

    @abstractmethod
    def perform_special_action(self, player):
        raise NotImplementedError

from abc import abstractmethod, ABCMeta


class Square:
    """
    Base class for all squares
    """
    def __init__(self, desc, number):
        self.__description = desc
        self.__number = number

    @property
    def description(self):
        """
        Description to be displayed
        """
        return self.__description

    @property
    def number(self):
        """
        Sequence number of a square
        """
        return self.__number

    @abstractmethod
    def perform_action(self, player):
        """
        Abstract method for generic action to be performed after landing on a square
        """
        raise NotImplementedError

    def __eq__(self, other):
        return self.__number == other.number and type(self) is type(other)

    def __str__(self):
        return "{} at {}".format(self.__class__.__name__, self.__number)


class GymSquare(Square, metaclass=ABCMeta):
    """
    Base class for gym squares that require player to stop on them
    """
    def __init__(self, desc, number):
        super(GymSquare, self).__init__(desc, number)


class SpecialSquare(Square, metaclass=ABCMeta):
    """
    Base class for special squares that require performing square's special action in the beginning of each turn
    """
    def __init__(self, desc, number):
        super(SpecialSquare, self).__init__(desc, number)

    @abstractmethod
    def perform_special_action(self, player):
        """
        Method performed in the beginning of each player turn starting from this square
        """
        raise NotImplementedError

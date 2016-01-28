from pokemon.gui.constants import Sex


class Player:
    """
    A player in the game.
    """

    def __init__(self, name, pokemon, age, sex=Sex.MALE):
        self.__name = name
        self.__pokemon = pokemon
        self.__drinks = []
        self.age = age
        self.sex = sex
        self.__fossil = None
        self.__status_ailments = []

    @property
    def name(self):
        """
        Name of the player
        """
        return self.__name

    @property
    def status(self):
        """
        Player's current status ailments
        """
        return self.__status_ailments

    def update_status(self):
        """Update player's status ailments and remove expired ailments."""
        for status in self.__status_ailments:
            status.update()
            if status.duration == 0:
                self.__status_ailments.remove(status)

    @property
    def drinks(self):
        """
        Amount of drink events player has had in the game
        """
        return sum([drink.number for drink in self.__drinks])

    @property
    def pokemon(self):
        """
        Player's current pokemon
        """
        return self.__pokemon

    @pokemon.setter
    def pokemon(self, pokemon):
        print("Changing {}'s pokemon from {} to {}".format(self.name, self.pokemon, pokemon))
        self.__pokemon = pokemon

    @property
    def fossil(self):
        """
        The fossil player has chosen. Empty by default, and set after event where Fossil is gained.
        """
        return self.__fossil

    @fossil.setter
    def fossil(self, fossil):
        self.__fossil = fossil

    def beats(self, other_player):
        """
        Function that determines which player has edge in battle via type effectiveness mechanics

        :param other_player Opponent pokemon trainer
        """
        return self.pokemon.beats(other_player.pokemon)

    def drink(self, drink):
        """
        Add drink event for a player

        :param drink Amount of drinks or a Drink class instance
        """
        if type(drink) is int:
            self.__drinks += [Drink(drink)]
        else:
            self.__drinks += [drink]

    def __eq__(self, other):
        return self.name == other.name and self.pokemon == other.pokemon

    def __str__(self):
        return "Player {} with pokemon {!s}".format(self.name, self.pokemon)

    def __hash__(self):
        return hash(repr(self))


class Drink:
    """
    Class representing an individual drink amount taken by e.g. an action at a square
    """
    def __init__(self, num):
        self.__number = num

    @property
    def number(self):
        """
        Number of drinks given in a drink event
        """
        return self.__number


class Fossil:
    pass


class DomeFossil(Fossil):
    # BURN THE FAKE GOD
    pass


class HelixFossil(Fossil):
    # ALL PRAISE LORD HELIX
    pass


class Players:
    """
    Class representing all players in the game and their play order.
    """
    def __init__(self, players):
        self.__players = players

    def current_player(self):
        return self.__players[0]

    def next(self):
        if len(self.__players) > 1:
            head, next_player, *tail = self.__players
            self.__players = [next_player] + tail + [head]
            return next_player
        else:
            return self.__players[0]

    def give_extra_turn(self):
        if len(self.__players) > 1:
            *init, last = self.__players
            self.__players = [last] + init

    def other_than(self, excluded_player):
        """Players other than the given one."""
        return [player for player in self.__players if player != excluded_player]

    def __str__(self):
        return [player.__str__() for player in self.__players].__str__()

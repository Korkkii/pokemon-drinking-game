from math import copysign
from pokemon.logic.square import GymSquare


class Player:
    def __init__(self, name, pokemon):
        self.__name = name
        self.__pokemon = pokemon
        self.__drinks = []
        self.__fossil = None

    @property
    def name(self):
        return self.__name

    @property
    def drinks(self):
        return self.__drinks

    @property
    def pokemon(self):
        return self.__pokemon

    @pokemon.setter
    def pokemon(self, pokemon):
        self.__pokemon = pokemon

    @property
    def fossil(self):
        return self.__fossil

    @fossil.setter
    def fossil(self, fossil):
        self.__fossil = fossil

    def beats(self, other_player):
        return self.pokemon.beats(other_player.pokemon)

    def drink(self, drink):
        self.__drinks += drink

class Drink:
    def __init__(self, num):
        self.__number = num

    @property
    def number(self):
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
    def __init__(self, players):
        self.__players = players

    def current_player(self):
        return self.__players[0]

    @property
    def next(self):
        head, *tail = self.__players
        self.__players = tail + head
        return head


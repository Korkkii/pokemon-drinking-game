from pokemon.logic.fight import Fight
from pokemon.logic.player import Players
from pokemon.logic.square import GymSquare
from pokemon.logic.throw import throw_dice


class GameBoard(dict):
    def __init__(self, squares, players):
        self.__squares = squares

        for player in players:
            self[player] = square[0]

    def __getattr__(self, player):
        if player in self:
            return self[player]
        else:
            raise AttributeError("No such attribute: " + player)

    def __setattr__(self, player, square):
        if square in self.__squares:
            self[player] = square

    def __delattr__(self, player):
        if player in self:
            del self[player]
        else:
            raise AttributeError("No such attribute: " + player)

    def players_in_square(self, target_square):
        for player, square in self.items():
            if target_square == square:
                yield player

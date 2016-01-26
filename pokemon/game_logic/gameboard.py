from pokemon.game_logic.fight import Fight
from pokemon.game_logic.player import Players
from pokemon.game_logic.square import GymSquare
from pokemon.game_logic.throw import throw_dice


class GameBoard(dict):
    def __init__(self, squares, players):
        super(GameBoard, self).__init__()
        self.__squares = squares

        for player in players:
            self[player] = squares[0]

    def players_in_square(self, target_square):
        for player, square in self.items():
            if target_square == square:
                yield player

from pokemon.logic.gameboard import GameBoard
from pokemon.logic.player import Players
from pokemon.logic.square import SpecialSquare


class Game:
    def __init__(self, squares, players):
        self.__board = GameBoard(squares, players)
        self.__players = Players(players)

    def play_turn(self):
        player = self.__players.current_player()
        if type(player.location) is SpecialSquare:
            player.location.perform_special_action(player)
        self.__board.play_player_turn(player)

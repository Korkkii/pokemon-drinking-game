from pokemon.logic.gameboard import GameBoard
from pokemon.logic.player import Players
from pokemon.logic.square import SpecialSquare


class Game:
    def __init__(self, squares, players, evManager):
        self.__board = GameBoard(squares, players)
        self.__players = Players(players)
        self.__player_order = Players(players)
        self.__ev_manager = evManager

    @property
    def players(self):
        return self.__player_order

    def play_player_turn(self, player):
        current = self.__board[player]
        if type(player.location) is SpecialSquare:
            player.location.perform_special_action(player)

        # Throw dice, and advance amount of throws, or until a gym square
        throw = throw_dice()

        for square_num in range(current.number, current.number + throw):
            current = self.__squares[square_num]
            if type(current) is GymSquare:
                break

        self.__players[player] = current

        # Fight all players in the destination square
        opponents = (fighter for fighter in self.__board.players_in_square(current) if fighter is not player)
        for opponent in opponents:
            Fight(player, opponent).start()

        # Perform action at square
        destination.perform_action()

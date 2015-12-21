from pokemon.logic.fight import Fight
from pokemon.logic.player import Players
from pokemon.logic.square import GymSquare
from pokemon.logic.throw import throw_dice


class GameBoard:
    def __init__(self, squares, players):
        self.__squares = squares
        self.__player_order = Players(players)
        self.__players = {}
        for player in players:
            self.__players[player] = self.__squares[0]

    @property
    def players(self):
        return self.__player_order

    def players_in_square(self, target_square):
        for player, square in self.__players:
            if target_square == square:
                yield player

    def play_player_turn(self, player):
        throw = throw_dice()
        current = player.location.number
        for square in range(current, current + throw):
            if type(square) is GymSquare:
                continue
        destination = player.move(throw)
        self.players[player] = destination
        fighters = self.players_in_square(destination)
        opponents = (fighter for fighter in fighters if fighter is not player)
        for opponent in opponents:
            Fight(player, opponent).start()
        destination.perform_action()

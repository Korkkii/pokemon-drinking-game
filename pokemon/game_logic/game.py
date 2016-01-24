from pokemon.game_logic.gameboard import GameBoard
from pokemon.game_logic.player import Players
from pokemon.game_logic.square import SpecialSquare
from pokemon.game_logic.throw import throw_dice
from pokemon.gui.event import PlayerMoved
from pokemon.gui.constants import Direction, DIRECTIONS, GAMEBOARD
from pygame.math import Vector2
from pokemon.game_logic.square import Square


class Game:
    def __init__(self, players, evManager):
        self.__players = Players(players)
        self.__ev_manager = evManager
        self.init_gameboard(players)

    def init_gameboard(self, players):
        direction_dict = {
            "U": Direction.UP,
            "R": Direction.RIGHT,
            "D": Direction.DOWN,
            "L": Direction.LEFT,
            "N": Direction.STATIONARY
        }

        squares = []
        start, finish = Vector2(0, 0)

        for j in range(9):
            row = []
            for i in [i for i in range(9)]:
                cell = GAMEBOARD[j][i]
                if cell == "S":
                    start = Vector2(i, j)
                    row.append(Direction.UP)
                elif cell == "F":
                    finish = Vector2(i, j)
                    row.append(Direction.STATIONARY)
                else:
                    row.append(direction_dict[cell])

            squares.append(row)

        current_coordinate = start
        current_direction = squares[int(current_coordinate.y)][int(current_coordinate.x)]
        self.game_coordinates = []
        self.board_squares = []
        index = 0
        while current_direction != Direction.STATIONARY and current_coordinate != finish:
            next_coordinate = current_coordinate + DIRECTIONS[current_direction]
            self.board_squares.append(Square("", index))
            self.game_coordinates.append(current_coordinate)
            # self.game_coordinates[index] = current_coordinate
            current_coordinate = next_coordinate
            current_direction = squares[int(current_coordinate.y)][int(current_coordinate.x)]
            index += 1

        self.gameboard = GameBoard(self.board_squares, players)

    def get_player_square(self, player):
        return self.gameboard[player]

    @property
    def current_player(self):
        return self.__player_order.current_player()

    def play_next_turn(self):
        current_player = self.__players.next()
        player_location = self.gameboard[current_player]
        # if type(player_location) is SpecialSquare:
        #     player.location.perform_special_action(player)

        # Throw dice, and advance amount of throws, or until a gym square
        throw = 1  # throw_dice()

        next_square = self.find_next_square(player_location.number, throw)
        self.gameboard[current_player] = self.board_squares[next_square]
        self.__ev_manager.post_event(PlayerMoved(current_player, next_square))

        # Fight all players in the destination square
        # opponents = (fighter for fighter in self.__board.players_in_square(current) if fighter is not player)
        # for opponent in opponents:
        #     Fight(player, opponent).start()

        # Perform action at square
        # destination.perform_action()

    def find_next_square(self, start, throw):
        current_square = start
        for square_num in range(start, start + throw + 1):
            current_square = square_num
            # if type(current) is GymSquare:
            #     break
        return current_square

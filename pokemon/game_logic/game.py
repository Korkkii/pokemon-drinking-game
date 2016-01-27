from pokemon.game_logic.gameboard import GameBoard
from pokemon.game_logic.player import Players
from pokemon.game_logic.square import SpecialSquare
from pokemon.game_logic.throw import throw_dice
from pokemon.game_logic.fight import Fight
from pokemon.gui.event import PlayerMoved, PlayersFought, OtherPlayersRequired, OtherPlayers
from pokemon.gui.constants import Direction, DIRECTIONS, GAMEBOARD
from pygame.math import Vector2
from pokemon.game_logic.square import GymSquare, Square
from pokemon.game_logic.squares import PidgeySquare
from concurrent.futures import ThreadPoolExecutor
from pokemon.game_logic.status_effects import GainTurn


class Game:
    def __init__(self, players, evManager):
        self.__players = Players(players)
        self.__ev_manager = evManager
        self.__ev_manager.register_listener(self)
        self.init_gameboard(players)
        self.events = []

    def init_gameboard(self, players):
        direction_dict = {
            "U": Direction.UP,
            "R": Direction.RIGHT,
            "D": Direction.DOWN,
            "L": Direction.LEFT,
            "GU": Direction.UP,
            "GR": Direction.RIGHT,
            "GD": Direction.DOWN,
            "GL": Direction.LEFT,
            "SU": Direction.UP,
            "SR": Direction.RIGHT,
            "SD": Direction.DOWN,
            "SL": Direction.LEFT,
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
            x, y = current_coordinate
            cell = GAMEBOARD[int(y)][int(x)]
            if cell.startswith("G"):
                self.board_squares.append(GymSquare("", index))
            elif cell.startswith("S") and cell != "S":
                self.board_squares.append(SpecialSquare("", index))
            else:
                self.board_squares.append(PidgeySquare("", index))
            self.game_coordinates.append(current_coordinate)
            current_coordinate = next_coordinate
            current_direction = squares[int(current_coordinate.y)][int(current_coordinate.x)]
            index += 1
        self.last_square = index
        self.gameboard = GameBoard(self.board_squares, players)

    def get_player_square(self, player):
        return self.gameboard[player]

    @property
    def current_player(self):
        return self.__players.current_player()

    def play_next_turn(self):
        # Get player and current location
        current_player = self.__players.next()
        player_location = self.gameboard[current_player]

        # Perform special action if on a special square
        try:
            player_location.perform_special_action(current_player)
        except AttributeError:
            pass

        # Throw dice, and advance amount of throws, or until a gym square
        throw = throw_dice()

        next_square = self.find_next_square(player_location.number, throw)
        destination = self.board_squares[next_square]
        self.gameboard[current_player] = destination
        self.__ev_manager.post_event(PlayerMoved(current_player, player_location.number, next_square))

        # Fight all players in the destination square
        opponents = [fighter for fighter in self.gameboard.players_in_square(next_square)
                     if fighter != current_player]
        fight_results = [Fight(current_player, opponent).start() for opponent in opponents]
        self.__ev_manager.post_event(PlayersFought(current_player, fight_results))

        # Get other players if needed in square action
        try:
            self.__ev_manager.post_event(OtherPlayersRequired(destination.other_players_required, next_square))

            with ThreadPoolExecutor() as executor:
                # Wait for players from user interaction
                future_event = executor.submit(self.wait_for_event, next_square)
                event = future_event.result(1)
                destination.other_players = event.players_required
        except (AttributeError, TimeoutError) as e:
            pass

        # Perform action at square
        destination.perform_action(current_player)

        # Give player an extra turn if gained one
        if any(isinstance(status, GainTurn) for status in current_player.status):
            self.__players.give_extra_turn()

        # Update player's status ailments
        current_player.update_status()

    def wait_for_event(self, square_num):
        while True:
            event_list = [event for event in self.events if event.square_num == square_num]
            if event_list is not None:
                return event_list[0]

    def find_next_square(self, start, throw):
        current_square = start
        for square_num in range(start + 1, start + throw + 1):
            current_square = square_num
            if type(self.board_squares[current_square]) is GymSquare:
                return current_square
        return current_square

    def notify(self, event):
        if isinstance(event, OtherPlayers):
            self.events.append(event)

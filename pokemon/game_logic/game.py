from pokemon.game_logic.gameboard import GameBoard
from pokemon.game_logic.player import Players
from pokemon.game_logic.square import SpecialSquare
from pokemon.game_logic.throw import throw_dice
from pokemon.game_logic.fight import Fight
from pokemon.gui.event import PlayerMoved, PlayersFought, OtherPlayersRequired, OtherPlayers
from pokemon.gui.constants import Direction, DIRECTIONS, GAMEBOARD
from pygame.math import Vector2
from pokemon.game_logic.square import GymSquare, Square
from pokemon.game_logic.squares import ClefairySquare
from concurrent.futures import ThreadPoolExecutor
from pokemon.game_logic.status_effects import GainTurn, SlowMovement, Confusion, LoseTurn, IncreaseMovement
from math import ceil
from pokemon.game_logic.square_mixins import RequireEverybodyExceptCurrentMixin, RequireAllMixin


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
                self.board_squares.append(Square("", index))
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

        # Check if misses turn
        if self.check_miss_turn(current_player):
            current_player.update_status()
            return

        # Perform special action if on a special square
        try:
            player_location.perform_special_action(current_player)
        except AttributeError:
            pass

        destination, throw = self.throw_dice_and_move(current_player, player_location)
        self.gameboard[current_player] = destination
        self.__ev_manager.post_event(PlayerMoved(current_player, player_location.number, destination.number))

        # Fight all players in the destination square
        opponents = [fighter for fighter in self.gameboard.players_in_square(destination.number)
                     if fighter != current_player]
        fight_results = [Fight(current_player, opponent).start() for opponent in opponents]
        self.__ev_manager.post_event(PlayersFought(current_player, fight_results))

        # If square action requires targeting others than current player
        square_action_throw = throw_dice()
        target_players = self.request_other_players(current_player, destination, square_action_throw)

        # Perform action at square
        destination.perform_action(current_player, target_players, all_squares=self.board_squares,
                                   throw=square_action_throw, gameboard=self.gameboard)

        # Give player an extra turn if gained one
        if any(isinstance(status, GainTurn) for status in current_player.status):
            self.__players.give_extra_turn()

        # Update player's status ailments
        current_player.update_status()

    def check_miss_turn(self, current_player):
        confusion = [status for status in current_player.status if isinstance(status, Confusion)]

        # Check confusion status
        if len(confusion) > 0:
            if throw_dice() not in confusion[0].stop_confuse_range:
                try:
                    current_player.drink(confusion[0].drink_amount)
                except AttributeError:
                    pass
                return True
            else:
                current_player.status.remove(confusion[0])
                return False

        # Check if player misses a turn
        elif any(isinstance(status, LoseTurn) for status in current_player.status):
            try:
                lose_status = next(isinstance(status, LoseTurnAndDrink) for status in current_player.status)
                current_player.drink(lose_status.drink_per_turn)
            except AttributeError:
                pass
            return True
        else:
            return False

    def throw_dice_and_move(self, current_player, current_location):
        # Throw dice, and advance amount of throws, or until a gym square
        throw = throw_dice()
        # Halve movement if has status SLowMovement
        if any(isinstance(status, SlowMovement) for status in current_player.status):
            throw = ceil(throw / 2)
        elif any(isinstance(status, IncreaseMovement) for status in current_player.status):
            throw *= 2

        next_square = self.find_next_square(current_location.number, throw)
        destination = self.board_squares[next_square]
        return (destination, throw)

    def request_other_players(self, current_player, destination, throw):
        """Request target players if needed in square action"""
        # Check if all players required
        if isinstance(destination, RequireAllMixin):
            return self.players
        else:
            # Check if other players are required based on throw
            try:
                if not destination.require_other_based_on_throw(throw):
                    return []
            except AttributeError:
                pass

        # Request users to choose targets
        try:
            self.__ev_manager.post_event(OtherPlayersRequired(destination.other_players_required, destination.number))

            with ThreadPoolExecutor() as executor:
                # Wait for players from user interaction
                future_event = executor.submit(self.wait_for_event, destination.number)
                event = future_event.result()
                return event.players_required
        except (AttributeError, TimeoutError) as e:
            # Does not need specific targets
            # Check if needs all others
            if isinstance(destination, RequireEverybodyExceptCurrentMixin):
                return self.__players.other_than(current_player)

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

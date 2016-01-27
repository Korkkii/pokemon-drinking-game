from pokemon.game_logic.square_mixins import DrinkMixin, ExtraTurnMixin, LoseTurnMixin, ReplacePokemonMixin, TeleportMixin, RequireOtherPlayersMixin
from pokemon.game_logic.square import GymSquare, Square


class RattataSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player):
        self.give_drinks(player, 10)


class PidgeySquare(Square, DrinkMixin, ExtraTurnMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        self.other_players_required = 1
        self.other_players = []
        self.turns = 1
        super().__init__(description, number)

    def perform_action(self, player):
        self.give_drinks(self.other_players[0], 1)
        self.gain_turn(player)

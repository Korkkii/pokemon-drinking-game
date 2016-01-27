from pokemon.game_logic.status_effects import GainTurn, LoseTurn


class DrinkMixin:
    def give_drinks(self, player, number):
        player.drink(number)


class ExtraTurnMixin:
    def gain_turn(self, player):
        player.status.append(GainTurn(self.turns))


class ReplacePokemonMixin:
    def replace_pokemon(self, player, pokemon):
        player.pokemon = pokemon


class LoseTurnMixin:
    def lose_turn(self, player):
        player.status.append(LoseTurn(self.turns))


class TeleportMixin:
    locations = []

    def __init__(self):
        self.locations.append(self.number)


class RequireOtherPlayersMixin:
    def __init__(self, player_number):
        self.other_players_required = 0
        self.other_players = []

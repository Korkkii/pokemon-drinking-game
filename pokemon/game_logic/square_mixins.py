from pokemon.game_logic.status_effects import GainTurn, LoseTurn, TripleGivenDrinks
from pokemon.game_logic.throw import throw_dice


class DrinkMixin:
    def give_drinks(self, player, number, giver=None):
        if giver is not None and any(isinstance(status, TripleGivenDrinks) for status in player.status):
            self.give_drinks(giver, number * 3)

        player.drink(number)


class ExtraTurnMixin:
    def gain_turn(self, player, for_turns):
        player.status.append(GainTurn(for_turns))


class ReplacePokemonMixin:
    def replace_pokemon(self, player, pokemon):
        player.pokemon = pokemon


class LoseTurnMixin:
    def lose_turn(self, player, for_turns):
        player.status.append(LoseTurn(for_turns))


class TeleportMixin:
    locations = []

    def __init__(self):
        self.locations.append(self.number)


class RequireOtherPlayersMixin:
    def __init__(self):
        self.other_players_required = 0
        self.other_players = []


class RequireEverybodyExceptCurrentMixin:
    pass


class RequireOtherBasedOnThrowMixin(RequireOtherPlayersMixin):
    def __init__(self):
        super().__init__()

    def require_other_based_on_throw(self, throw):
        pass


class RequireAllMixin:
    pass


class RequireAllSquaresMixin:
    pass


class PokemonTowerMixin:
    def perform_special_action(self, player):
        pass


class SilphCoMixin:
    def perform_special_action(self, player):
        player.drink(2)


class SafariZoneMixin:
    def perform_special_action(self, player):
        throw = throw_dice()
        # TODO: Give from Mixin
        if throw in [1, 2]:
            # Give to player
            pass
        elif throw in [3, 4]:
            player.status.append(LoseTurn(1))
            player.drink(4)
        else:
            player.drink(2)

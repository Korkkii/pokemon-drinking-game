from pokemon.game_logic.pokemon_character import Pikachu
from pokemon.game_logic.square import GymSquare, SpecialSquare, Square
from pokemon.game_logic.square_mixins import (DrinkMixin,
                                              RequireEverybodyExceptCurrentMixin,
                                              ExtraTurnMixin, LoseTurnMixin,
                                              ReplacePokemonMixin,
                                              RequireAllMixin, RequireAllSquaresMixin,
                                              RequireOtherBasedOnThrowMixin,
                                              RequireOtherPlayersMixin,
                                              TeleportMixin, PokemonTowerMixin, SilphCoMixin, SafariZoneMixin)
from pokemon.game_logic.status_effects import Confusion, SlowMovement, IncreaseMovement, LoseTurnAndDrink, SkipGym, DrinkInConfusion, DrinkImmunity, EliteFourChallenge
from random import randint
from math import ceil
from pokemon.game_logic.throw import throw_dice


class RattataSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 10)


class PidgeySquare(Square, DrinkMixin, ExtraTurnMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 1
        self.other_players = []
        self.turns = 1

    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(target_players[0], 1, player)
        self.gain_turn(player, 1)


class CaterpieSquare(Square, RequireEverybodyExceptCurrentMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.all_other_players = []

    def perform_action(self, player, all_other_players, *args, **kwargs):
        for other_player in all_other_players:
            player.status.append(SlowMovement(1))


class PikachuSquare(Square, ReplacePokemonMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.replace_pokemon(player, Pikachu())


class BeedrillSquare(Square, DrinkMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 2
        self.other_players = []

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)


class PewterCityGym(GymSquare, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 1
        self.other_players = []

    def perform_action(self, player, target_players, *args, **kwargs):
        if len(target_players) == 0:
            self.give_drinks(player, 1)
        else:
            for target in target_players:
                self.give_drinks(target, 1, player)

    def require_other_based_on_throw(self, throw):
        if throw % 2 == 0:
            return True
        else:
            return False


class NidoranSquare(Square, DrinkMixin, RequireAllMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            if player.sex == target.sex:
                self.give_drinks(target, 1, player)


class ZubatSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 1)
        player.status.append(DrinkInConfusion([3, 4, 5, 6], 1))


class ClefairySquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        amount = randint(1, 10)
        self.give_drinks(player, amount)


class JigglypuffSquare(Square, ExtraTurnMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.gain_turn(player, 1)


class AbraSquare(Square, TeleportMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.locations.append(number)

    def perform_action(self, player, *args, **kwargs):
        super().perform_action(player, *args, **kwargs)
        # TODO: Implement teleport movement


class GaryFirstSquare(Square, DrinkMixin, RequireOtherBasedOnThrowMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 0
        self.other_players = []

    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, ceil(kwargs["throw"] / 2))
        for target in target_players:
            self.give_drinks(target, 1, player)

    def require_other_based_on_throw(self, throw):
        amount = ceil(throw / 2)
        self.other_players_required = amount
        return True


class CeruleanCityGym(GymSquare, DrinkMixin, RequireEverybodyExceptCurrentMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, 2)
        for target in target_players:
            self.give_drinks(target, 1, player)


class BellsproutSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 1)


class MeowthSquare(Square, DrinkMixin, RequireEverybodyExceptCurrentMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)


class DiglettSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        amount = 10 - (player.drinks % 10)
        self.give_drinks(player, amount)


class SSAnneSquare(Square, DrinkMixin, LoseTurnMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        lose_turn_throw = kwargs["throw"]
        drink_throw = throw_dice
        self.give_drinks(player, amount)
        player.status.append(LoseTurnAndDrink(lose_turn_throw, drink_throw))


class VermilionCityGym(Square, DrinkMixin, LoseTurnMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        throw = kwargs["throw"]
        if throw % 2 == 0:
            self.give_drinks(player, 2)
            self.lose_turn(player, 1)
        else:
            self.give_drinks(player, 1)


class BicycleSquare(Square):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        player.status.append(IncreaseMovement(1))


class MagikarpSquare(Square):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class SandshrewSquare(Square):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class PokemonTowerSquare(SpecialSquare, PokemonTowerMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class ChannelerSquare(SpecialSquare, PokemonTowerMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class HaunterSquare(SpecialSquare, PokemonTowerMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 1
        self.other_players = []

    def perform_action(self, player, target_players, *args, **kwargs):
        # TODO: Move animation 10 squares backwards
        pass


class CuboneSquare(SpecialSquare, PokemonTowerMixin, RequireAllMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            target.drink(1)


class GhostSquare(SpecialSquare, PokemonTowerMixin, RequireEverybodyExceptCurrentMixin, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        gameboard = kwargs["gameboard"]
        players_in_silph = [target for target in target_players if isinstance(gameboard[target], SilphCoMixin)]
        if len(players_in_silph) > 0:
            for target in target_players:
                self.give_drinks(target, 1, player)
        else:
            self.give_drinks(player, 3)


class SnorlaxSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        # Implement "choose sing or drink 4"
        pass


class GarySecondSquare(Square, DrinkMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, kwargs["throw"] - 1)


class EeveeSquare(Square):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class CeladonCityGym(GymSquare, LoseTurnMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        throw = kwargs["throw"]
        if throw <= 3:
            self.lose_turn(player, 1)
        else:
            amount = 10 - (player.drinks % 10)
            self.give_drinks(player, amount)


class PsyduckSquare(Square):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class EvolutionSquare(Square, DrinkMixin, ExtraTurnMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        # TODO: Implement Choice
        if True:
            self.give_drinks(player, 4)
            player.status.append(SkipGym())
        else:
            self.gain_turn(player, 1)


class PorygonSquare():
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        player.status.append(TripleGivenDrinks(1))


class SilphCoSquare(SpecialSquare, SilphCoMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        pass


class ScientistSquare(SpecialSquare, SilphCoMixin, DrinkMixin, RequireEverybodyExceptCurrentMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, len(target_players))


class LaprasSquare(SpecialSquare, SilphCoMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, *args, **kwargs):
        player.status.append(Confusion([1, 2, 3]))


class TeamRocketSquare(SpecialSquare, SilphCoMixin, DrinkMixin, RequireAllMixin):
    def __init__(self, description, number):
        super().__init__(description, number)

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)


class GiovanniSquare(SpecialSquare, SilphCoMixin, DrinkMixin, RequireOtherBasedOnThrowMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 0

    def perform_action(self, player, target_players, *args, **kwargs):
        throw = kwargs["throw"]
        if len(target_players) > 0:
            for target in target_players:
                self.give_drinks(target, 1, player)
        else:
            self.give_drinks(player, throw)

    def require_other_based_on_throw(self, throw):
        if throw <= 3:
            self.other_players_required = throw
            return True
        else:
            return False


class RareCandySquare(Square, ExtraTurnMixin):
    def perform_action(self, player, *args, **kwargs):
        self.gain_turn(player, 1)


class GaryThirdSquare(Square, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, kwargs["throw"])


class SaffronCityGym(GymSquare, DrinkMixin, ExtraTurnMixin):
    def perform_action(self, player, *args, **kwargs):
        # TODO: Add pick a number and check if correct
        if throw == 0:
            self.gain_turn(player, 1)
        else:
            self.give_drinks(player, 2)


class FightGymSquare(Square, LoseTurnMixin, ExtraTurnMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 1

    def perform_action(self, player, target_players, *args, **kwargs):
        # TODO: Who wins chugging contest
        if player is "first":
            self.gain_turn(player, 1)
            self.lose_turn(target_players[0], 1)
        else:
            self.gain_turn(target_players[0], 1)
            self.lose_turn(player, 1)


class KrabbySquare(Square, DrinkMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 1

    def perform_action(self, player, target_players, *args, **kwargs):
        target = target_players[0]
        amount = 10 - (target.drinks % 10)
        self.give_drinks(target, amount, player)


class DittoSquare(Square):
    def perform_action(self, player, *args, **kwargs):
        # TODO: Implement ditto of status
        pass


class DoduoSquare(Square, DrinkMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 4

    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, 1)
        for target in target_players:
            self.give_drinks(target, 1, player)


class SafariZoneSquare(SpecialSquare, SafariZoneMixin):
    def perform_action(self, player, *args, **kwargs):
        pass


class TaurusSquare(SpecialSquare, SafariZoneMixin, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 2)


class DoduoSquare(Square, DrinkMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 2

    def perform_action(self, player, target_players, *args, **kwargs):
        throw = kwargs["throw"]
        if throw <= 3:
            self.give_drinks(player, 1)
        else:
            for target in target_players:
                self.give_drinks(target, 1, player)


class FuchsiaCityGym(GymSquare, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 3)


class ElectrodeSquare(Square, DrinkMixin, RequireAllMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            amount = 10 - (target.drinks % 10)
            self.give_drinks(target, amount)


class ElectabuzzSquare(Square, LoseTurnMixin):
    def perform_action(self, player, *args, **kwargs):
        self.lose_turn(player, 1)


class PoliwagSquare(Square, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        self.give_drinks(player, 10)


class SeakingSquare(Square, DrinkMixin, RequireAllMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 5)


class MissignoSquare(Square):
    # TODO: Implement back to start
    pass


class CinnabarCityGym(GymSquare, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        last_roll = throw_dice()
        rolls = [last_roll]
        while last_roll % 2 == 0:
            roll = throw_dice()
            rolls.append(roll)
            last_roll = roll
        self.give_drinks(player, len(rolls))


class KoffingSquare(Square, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        # TODO: Implement Choice drinking
        self.give_drinks(player, 2)


class FossilSquare(Square, DrinkMixin, RequireAllMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        older = [target for target in target_players if player.age < target.age]
        for old in older:
            self.give_drinks(old, 1, player)


class PokeballSquare(Square, DrinkMixin):
    def perform_action(self, player, *args, **kwargs):
        throw = kwargs["throw"]
        if throw > 3:
            self.give_drinks(player, 2)


class PersianSquare(Square, RequireOtherBasedOnThrowMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 0

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)

    def require_other_based_on_throw(self, throw):
        self.other_players_required = throw
        return True


class ViridianCityGym(GymSquare, DrinkMixin, RequireAllMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, 1)
        same_sex = [target for target in target_players if player.sex == target.sex]
        for target in same_sex:
            self.give_drinks(target, 3, player)


class FearowSquare(Square, DrinkMixin):
    # TODO: Implement action based on last player
    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)


class GravelerSquare(Square, LoseTurnMixin):
    def perform_action(self, player, *args, **kwargs):
        self.lose_turn(player, 2)
        player.status.append(DrinkImmunity(2))


class GyaradosSquare(Square, DrinkMixin):
    # TODO: Require players based on status
    def perform_action(self, player, *args, **kwargs):
        if any(isinstance(status, VisitedMagikarp) for status in player.status):
            # Give drinks
            pass
        else:
            self.give_drinks(player, 4)


class DragoniteSquare(Square, LoseTurnMixin, DrinkMixin, RequireOtherPlayersMixin):
    def __init__(self, description, number):
        super().__init__(description, number)
        self.other_players_required = 5

    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1, player)
            self.lose_turn(player, 1)


class BirdsSquare(GymSquare, DrinkMixin):
    # TODO: Implement wait until all 3 caught
    def perform_action(self, player, target_players, *args, **kwargs):
        pass


class EliteFourSquare(GymSquare, DrinkMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        throw = kwargs["throw"]
        if throw not in [4]:
            self.give_drinks(player, 4)
        # player.status.append(EliteFourChallenge([4], 4))


class ChampionGarySquare(GymSquare, DrinkMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        self.give_drinks(player, 10)


class PokemonMasterSquare(GymSquare, DrinkMixin, RequireEverybodyExceptCurrentMixin):
    def perform_action(self, player, target_players, *args, **kwargs):
        for target in target_players:
            self.give_drinks(target, 1)

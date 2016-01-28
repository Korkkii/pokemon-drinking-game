class StatusEffect:
    def __init__(self, turns):
        self.duration = turns

    def update(self):
        self.duration -= 1


class LoseTurn(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class LoseTurnAndDrink(LoseTurn):
    def __init__(self, turns, drink_per_turn):
        super().__init__(turns)
        self.drinks_per_turn = drink_per_turn


class GainTurn(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class SlowMovement(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class IncreaseMovement(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class Confusion(StatusEffect):
    def __init__(self, stop_range):
        super().__init__(100)
        self.stop_confuse_range = stop_range


class DrinkInConfusion(Confusion):
    def __init__(self, stop_range, drink_amount):
        super().__init__(stop_range)
        self.drink_amount = drink_amount


class SkipGym(StatusEffect):
    def __init__(self):
        super().__init__(100)


class TripleGivenDrinks(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class DrinkImmunity(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class VisitedMagikarp(StatusEffect):
    def __init__(self):
        super().__init__(1000)


class EliteFourChallenge(DrinkInConfusion):
    def __init__(self, stop_range, drink_amount):
        super().__init__(stop_range, drink_amount)

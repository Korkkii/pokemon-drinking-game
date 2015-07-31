from pokemon.logic.player import Drink
from pokemon.logic.throw import throw_dice_twice, throw_dice


class Fight:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start(self):
        if self.player1.beats(self.player2):
            self.give_drinks(throw_dice_twice(), throw_dice())
        elif self.player2.beats(self.player1):
            self.give_drinks(throw_dice(), throw_dice_twice())
        else:
            self.give_drinks(throw_dice(), throw_dice())

    def give_drinks(self, p1_throw, p2_throw):
        if p1_throw > p2_throw:
            self.player2.drink(Drink(2))
        elif p1_throw < p2_throw:
            self.player1.drink(Drink(2))
        else:
            self.player1.drink(Drink(1))
            self.player2.drink(Drink(1))

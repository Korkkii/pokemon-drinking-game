from pokemon.logic.player import Drink
from pokemon.logic.throw import throw_dice_twice, throw_dice


class Fight:
    """
    A single fight instance with two participants.
    """
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start(self):
        if self.player1.beats(self.player2):
            return self.FightResults(self.player1, self.player2, throw_dice_twice(), throw_dice())
        elif self.player2.beats(self.player1):
            return self.FightResults(self.player1, self.player2, throw_dice(), throw_dice_twice())
        else:
            return self.FightResults(self.player1, self.player2, throw_dice(), throw_dice())

    def give_drinks(self, p1_throw, p2_throw):
        if p1_throw > p2_throw:
            self.player2.drink(Drink(2))
        elif p1_throw < p2_throw:
            self.player1.drink(Drink(2))
        else:
            self.player1.drink(Drink(1))
            self.player2.drink(Drink(1))

    class FightResults:
        """
        Results of a fight instance
        """
        def __init__(self, player1, player2, player1_throws, player2_throws):
            self.__draw = None
            self.__draw_throw = None
            print(player1_throws)
            print(player2_throws)
            if max(player1_throws) > max(player2_throws):
                self.__winner = player1
                self.__winner_throws = player1_throws
                self.__loser = player2
                self.__loser_throws = player2_throws
            elif max(player2_throws) > max(player1_throws):
                self.__winner = player2
                self.__winner_throws = player2_throws
                self.__loser = player1
                self.__loser_throws = player1_throws
            else:
                self.__winner = None
                self.__loser = None
                self.__draw = player1, player2
                self.__draw_throw = player1_throws

        @property
        def winner(self):
            """
            Winner if there was no draw.
            """
            return self.__winner

        @property
        def winner_throws(self):
            """
            Winner's throw or throws if there was no draw.
            """
            return self.__winner_throws

        @property
        def loser(self):
            """
            Loser if there was no draw.
            """
            return self.__loser

        @property
        def loser_throws(self):
            """
            Loser's throw or throws if there was no draw.
            """
            return self.__loser_throws

        @property
        def draw(self):
            """
            Both players if there was a draw
            """
            return self.__draw

        @property
        def draw_throw(self):
            """
            The throw that resulted in draw
            """
            return self.__draw_throw


from pokemon.game_logic.player import Drink
from pokemon.game_logic.throw import throw_dice_twice, throw_dice


class Fight:
    """
    A single fight instance with two participants.

    A fight instance, where pokemons of trainers fight. Fight is resolved by die throws, where the trainer with
    type advantage gets best of two throws instead of a single throw. Loser of the fight drinks, unless there's a tie
    in which case both drink.
    """
    def __init__(self, player1, player2):
        """
        Fight class constructor.

        player1     First participant
        player2     Second participant
        """

        self.__player1 = player1
        self.__player2 = player2

    def start(self):
        """
        Fight starter.

        Starts the fight between players with type advantages taken into account. Gives drinks to loser, or both in
        case of a tie.

        returns     Fight results
        """

        if self.__player1.beats(self.__player2):
            result = FightResults(self.__player1, self.__player2, throw_dice_twice(), [throw_dice()])
        elif self.__player2.beats(self.__player1):
            result = FightResults(self.__player1, self.__player2, [throw_dice()], throw_dice_twice())
        else:
            result = FightResults(self.__player1, self.__player2, [throw_dice()], [throw_dice()])

        # Loser drinks 2, or both drink 1 if tie
        if result.draw is None:
            result.loser.drink(Drink(2))
        else:
            result.draw[0].drink(Drink(1))
            result.draw[1].drink(Drink(1))

        return result


class FightResults:
    """
    Results of a fight instance.

    Results of a single fight instance. The results contain be throws of each player, who won and lost, and tie
    information.
    """
    def __init__(self, player1, player2, player1_throws, player2_throws):
        """
        Fight results with throw information

        player1         Player 1
        player2         Player 2
        player1_throws  List of player 1's throws
        player2_throws  List of player 2's throws
        """
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

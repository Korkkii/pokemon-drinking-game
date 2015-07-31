from unittest.mock import patch
from pokemon.logic.fight import Fight
from pokemon.logic.player import Player
from pokemon.logic.pokemon_character import Charmander, Bulbasaur, Squirtle


@patch("pokemon.logic.fight.throw_dice", side_effects=[[1], [1]])
def test_no_winner_or_loser_values_with_draw(mock_randint):
    player1 = Player("tester1", Charmander())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.winner is None
    assert fight_results.loser is None
    assert player1 in fight_results.draw and player2 in fight_results.draw
    assert fight_results.draw == 1


@patch("pokemon.logic.fight.throw_dice", side_effects=[[2], [1]])
def test_no_draw_values_with_winner(mock_randint):
    player1 = Player("tester1", Charmander())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.draw is None
    assert fight_results.draw_throw is None
    assert fight_results.winner is not None
    assert fight_results.loser is not None


@patch("pokemon.logic.fight.throw_dice", side_effects=[[5], [1]])
def test_player1_wins_single_rolls(mock_randint):
    player1 = Player("tester1", Charmander())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.winner == player1
    assert fight_results.winner_throws == 5
    assert fight_results.loser == player2
    assert fight_results.loser_throws == 1


@patch("pokemon.logic.fight.throw_dice", side_effects=[[2], [3]])
def test_player2_wins_single_rolls(mock_randint):
    player1 = Player("tester1", Charmander())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.winner == player2
    assert fight_results.winner_throws == 3
    assert fight_results.loser == player1
    assert fight_results.loser_throws == 2


@patch("pokemon.logic.fight.throw_dice", return_value=[3])
@patch("pokemon.logic.fight.throw_dice_twice", return_value=[1, 5])
def test_player1_wins_double_rolls(mock_throw, mock_throw_twice):
    player1 = Player("tester1", Squirtle())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.winner == player1
    assert fight_results.winner_throws == [1, 5]
    assert fight_results.loser == player2
    assert fight_results.loser_throws == [3]


@patch("pokemon.logic.fight.throw_dice", return_value=[5])
@patch("pokemon.logic.fight.throw_dice_twice", return_value=[1, 6])
def test_player2_wins_double_rolls(mock_throw, mock_throw_twice):
    player1 = Player("tester1", Bulbasaur())
    player2 = Player("tester2", Charmander())
    fight = Fight(player1, player2)

    fight_results = fight.start()
    assert fight_results.winner == player2
    assert fight_results.winner_throws == [1, 6]
    assert fight_results.loser == player1
    assert fight_results.loser_throws == [5]

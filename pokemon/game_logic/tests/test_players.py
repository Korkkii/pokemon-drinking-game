from pokemon.game_logic.player import Players, Player
from pokemon.game_logic.pokemon_character import Squirtle


def test_current_player():
    player1 = Player("tester1", Squirtle())
    player2 = Player("tester2", Squirtle())
    player3 = Player("tester3", Squirtle())
    players = Players([player1, player2, player3])

    assert players.current_player() == player1
    players.next()
    assert players.current_player() == player2
    players.next()
    assert players.current_player() == player3
    players.next()
    assert players.current_player() == player1


def test_next_player():
    player1 = Player("tester1", Squirtle())
    player2 = Player("tester2", Squirtle())
    player3 = Player("tester3", Squirtle())
    players = Players([player1, player2, player3])

    assert players.current_player() == player1
    assert players.next() == player2
    assert players.next() == player3
    assert players.next() == player1

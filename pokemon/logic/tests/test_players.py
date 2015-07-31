from pokemon.logic.player import Players, Player
from pokemon.logic.pokemon_character import Squirtle


def test_current_player():
    players = Players([Player("tester1", Squirtle()), Player("tester2", Squirtle()), Player("tester3", Squirtle())])
    
    assert players.current_player().name() == "tester1"
    players.next()
    assert players.current_player().name() == "tester2"
    players.next()
    assert players.current_player().name() == "tester3"
    players.next()
    assert players.current_player().name() == "tester1"

def test_next_player():
    players = Players([Player("tester1", Squirtle()), Player("tester2", Squirtle()), Player("tester3", Squirtle())])

    assert players.next() == "tester2"
    assert players.next() == "tester3"
    assert players.next() == "tester1"

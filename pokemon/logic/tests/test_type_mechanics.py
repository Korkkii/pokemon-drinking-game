# Test pokemon fighting type mechanics
from nose.tools import assert_true, assert_false
from pokemon.logic.pokemon_character import Charmander, Squirtle, Bulbasaur


def test_super_effective():
    pokemons = [Charmander(), Squirtle(), Bulbasaur()]
    *firsts, last = pokemons
    pairs = list(zip(pokemons, [last] + firsts))

    for pkmn1, pkmn2 in pairs:
        assert_true(pkmn1.beats(pkmn2))
        assert_false(pkmn2.beats(pkmn1))


def test_normal_effective():
    pokemons = [Charmander(), Squirtle(), Bulbasaur()]
    pairs = list(zip(pokemons, pokemons))

    for pkmn1, pkmn2 in pairs:
        assert_false(pkmn1.beats(pkmn2))
        assert_false(pkmn2.beats(pkmn1))


def test_not_very_effective():
    pokemons = [Charmander(), Squirtle(), Bulbasaur()]
    head, *tail = pokemons
    pairs = list(zip(pokemons, tail + [head]))

    for pkmn1, pkmn2 in pairs:
        assert_true(pkmn2.beats(pkmn1))
        assert_false(pkmn1.beats(pkmn2))

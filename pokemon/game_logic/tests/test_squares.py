from unittest import patch, TestCase
from pokemon.game_logic.squares import *
from pokemon.game_logic.player import Player, Players
from pokemon.game_logic.pokemon_character import Bulbasaur, Charmander, Squirtle, Pikachu
from pokemon.game_logic.status_effects import SlowMovement
from pokemon.gui.constants import Sex


class SquaresTest(TestCase):
    def setUp(self):
        self.players = [Player("tester1", Charmander(), Sex.MALE), Player("tester2", Bulbasaur(), Sex.MALE),
                        Player("tester3", Squirtle(), Sex.FEMALE)]
        self.player_order = Players(self.players)

    def test_rattata(self):
        square = RattataSquare("", 0)
        current_player = self.player_order.next()
        square.perform_action(current_player)
        self.assertTrue(current_player.drinks == 10)

    def test_pidgey(self):
        square = PidgeySquare("", 0)
        current_player = self.player_order.next()
        target_players = self.player_order.other_than(current_player)[0:1]
        square.perform_action(current_player, target_players)

        self.assertTrue(target_players[0].drinks == 1)
        self.assertEqual(self.player_order.next(), current_player)

    def test_pikachu(self):
        square = CaterpieSquare("", 0)
        current_player = self.player_order.next()
        target_players = self.player_order.other_than(current_player)
        square.perform_action(current_player, target_players)

        self.assertTrue(all(any(isinstance(status, SlowMovement) for status in target.status)
                        for target in target_players))

    def test_pikachu(self):
        square = PikachuSquare("", 0)
        current_player = self.player_order.next()
        target_players = self.player_order.other_than(current_player)
        square.perform_action(current_player)

        self.assertEqual(current_player.pokemon, Pikachu())

    def test_beedrill(self):
        square = PikachuSquare("", 0)
        current_player = self.player_order.next()
        target_players = self.player_order.other_than(current_player)[0:2]
        square.perform_action(current_player, target_players)

        self.assertTrue(all(target.drinks == 1 for target in target_players))

    def test_pewter_target_drinks(self):
        square = PewterCityGym("", 0)
        current_player = self.player_order.next()
        target_players = self.player_order.other_than(current_player)[0:1]

        square.perform_action(current_player, target_players)
        self.assertEqual(target_players[0].drinks, 1)
        self.assertEqual(current_player.drinks, 0)

    def test_pewter_player_drinks(self):
        square = PewterCityGym("", 0)
        current_player = self.player_order.next()

        square.perform_action(current_player, [])
        self.assertEqual(current_player.drinks, 1)

    def test_nidoran(self):
        square = NidoranSquare("", 0)
        current_player = self.player_order.next()
        targets = self.players

        square.perform_action(current_player, targets)
        same_sex = [player for player in self.players if player.sex == current_player.sex]
        self.assertTrue(all(player.drink == 1 for player in same_sex))

from game_logic.pokemon_type import Fire, Water, Grass, Electric


class PokemonBase:
    """
    Pokemon super class that defines base behaviour for all pokemons
    """
    @property
    def name(self):
        """
        Name of pokemon
        """
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def pkmn_type(self):
        """
        Type of pokemon
        """
        return self.__pkmn_type

    @pkmn_type.setter
    def pkmn_type(self, type):
        self.__pkmn_type = type

    def beats(self, enemy_pkmn):
        """
        Determines is the pokemon super effective against another pokemon via type mechanics

        :param enemy_pkmn Opponent pokemon
        """
        return self.pkmn_type.beats(enemy_pkmn.pkmn_type)

    def __str__(self):
        return self.name


class FirePokemon(PokemonBase):
    """
    Base class for fire pokemon
    """
    def __init__(self):
        self.pkmn_type = Fire()
        super().__init__()


class WaterPokemon(PokemonBase):
    """
    Base class for water pokemon
    """
    def __init__(self):
        self.pkmn_type = Water()
        super().__init__()


class GrassPokemon(PokemonBase):
    """
    Base class for grass pokemon
    """
    def __init__(self):
        self.pkmn_type = Grass()
        super().__init__()


class ElectricPokemon(PokemonBase):
    """
    Base class for electric pokemon
    """
    def __init__(self):
        self.pkmn_type = Electric()
        super().__init__()


class Charmander(FirePokemon):
    def __init__(self):
        self.name = "Charmander"
        super().__init__()


class Squirtle(WaterPokemon):
    def __init__(self):
        self.name = "Squirtle"
        super().__init__()


class Bulbasaur(GrassPokemon):
    def __init__(self):
        self.name = "Bulbasaur"
        super().__init__()


class Pikachu(ElectricPokemon):
    def __init__(self):
        self.name = "Pikachu"
        super().__init__()

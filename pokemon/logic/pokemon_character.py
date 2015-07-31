from pokemon.logic.pokemon_type import Fire, Water, Grass, Electric


class PokemonBase:
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def pkmn_type(self):
        return self.__pkmn_type

    @pkmn_type.setter
    def pkmn_type(self, type):
        self.__pkmn_type = type

    def beats(self, enemy_pkmn):
        return self.pkmn_type.beats(enemy_pkmn.pkmn_type)


class FirePokemon(PokemonBase):
    def __init__(self):
        self.pkmn_type = Fire()
        super().__init__()
    
    
class WaterPokemon(PokemonBase):
    def __init__(self):
        self.pkmn_type = Water()
        super().__init__()


class Charmander(FirePokemon):
    def __init__(self):
        self.name = "Charmander"
        super().__init__()


class Squirtle(WaterPokemon):
    def __init__(self):
        self.name = "Squirtle"
        super().__init__()


class GrassPokemon(PokemonBase):
    def __init__(self):
        self.pkmn_type = Grass()
        super().__init__()


class Bulbasaur(GrassPokemon):
    def __init__(self):
        self.name = "Bulbasaur"
        super().__init__()


class ElectricPokemon(PokemonBase):
    def __init__(self):
        self.pkmn_type = Electric()
        super().__init__()


class Pikachu(ElectricPokemon):
    def __init__(self):
        self.name = "Pikachu"
        super().__init__()

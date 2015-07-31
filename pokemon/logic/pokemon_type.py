class Type:
    def __init__(self, pokemon_type):
        self.pokemon_type = pokemon_type

    @property
    def pokemon_type(self):
        return self.__pokemon_type

    @pokemon_type.setter
    def pokemon_type(self, new_type):
        self.__pokemon_type = new_type

    def beats(self, other_type):
        return type(other_type) in __type_mechanics__[self.pokemon_type]


class Fire(Type):
    def __init__(self):
        super().__init__(Fire)


class Water(Type):
    def __init__(self):
        super().__init__(Water)


class Grass(Type):
    def __init__(self):
        super().__init__(Grass)


class Electric(Type):
    def __init__(self):
        super().__init__(Electric)

# Which types given type is super effective against
__type_mechanics__ = {
    Fire: [Grass],
    Grass: [Water],
    Water: [Fire],
    Electric: [Water]
}
class StatusEffect:
    def __init__(self, turns):
        self.duration = turns

    def update(self):
        self.duration -= 1


class LoseTurn(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)


class GainTurn(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)

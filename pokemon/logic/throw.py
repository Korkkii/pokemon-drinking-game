import random


def throw_dice():
    return random.randint(1, 6)


def throw_dice_twice():
    return max(throw_dice(), throw_dice())
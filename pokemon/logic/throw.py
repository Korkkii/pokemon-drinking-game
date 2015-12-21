import random


def throw_dice():
    """
    Generates a die throw between 1-6

    :returns the roll
    """
    return random.randint(1, 6)


def throw_dice_twice():
    """
    Generates two dice throws

    :returns list with both rolls
    """
    return [throw_dice(), throw_dice()]

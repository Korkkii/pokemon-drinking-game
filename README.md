# Pokemon Drinking Boardgame

## What is this

A personal project on learning basics of game and game engine development using Python 3 and PyGame. My main focus in this project is to learn what kinds of design patterns are used in development of games and game engines, and how they affect the quality of the code.

Materials used in learning process include:
1. [Gaming Programming Patterns by Robert Nystrom](http://gameprogrammingpatterns.com/)
2. [Writing Games by Shandy Brown](http://ezide.com/games/writing-games.html)

## Disclaimer

I do not own the Pokemon franchise (property of Nintendo) nor the [assets I'm using](pokemon/gui/assets/README.md). Only the code here is mine.

## Requirements

The game requires [PyGame](http://pygame.org/) 1.9.1 or newer, and Python 3.

## How to run

Using command line and Python 3.

```bash
$ cd path/to/pokemon-drinking-game
$ python -m pokemon.main
```

## TODO

- [ ] Game Logic
    - [x] Player
    - [x] Pokemon types
    - [x] Player battles
    - [x] Gameboard
    - [ ] Square mechanics
        - [x] Drink
        - [x] Gain turn
        - [ ] Lose turn
        - [ ] Replace pokemon
        - [ ] Teleport
        - [x] Require other players
    - [ ] Status ailments
        - [x] Turn gain / lose
- [ ] Graphical User Interface
    - [x] Player sprite
        - [x] Animated sprite
        - [x] Movable player sprite
        - [x] Multiple movable sprites
    - [x] Gameboard
        - [x] Move players on the board
    - [ ] Game status
        - [ ] Score screen
        - [ ] Fight results
    - [ ] Game starter screen
        - [ ] Add players with names and their pokemon
- [ ] Integrate game logic with GUI
    - [x] Player movement
    - [x] Player battles
    - [ ] Game status
- [ ] Future plans
    - [ ] Pokemon evolution
    - [ ] Pokemon capturing

# Ren'Py Chess Engine 2.0

## About

This is a chess GUI built with the [Ren'Py](http://renpy.org/) Visual Novel Engine, [python-chess](https://github.com/niklasf/python-chess), and [Stockfish](https://stockfishchess.org/) (for chess AI).

### Gameplay Example: Fool's Mate
<img src="https://github.com/RuolinZheng08/renpy-chess/blob/master/gif-demo/foolsmate.gif" alt="Gameplay Example" width=600>

## Gameplay

The game supports **Player vs. Player** and **Player vs. Computer**. In PvC, player can choose to play as either Black or White.

Click on a piece and all of its available moves will be highlighted. Click on any of the legal destination squares to make a move. Press `Flip board view` to flip the view, with White on the bottom by default.

### Feature List
- PvP and PvC
- Flip board view
- Resign
- Undo moves

#### Player vs. Computer (Stockfish)
<img src="https://github.com/RuolinZheng08/renpy-chess/blob/master/gif-demo/pvc.gif" alt="Play vs Computer" width=600>

#### Flip Board View, Undo Moves, Resign
<img src="https://github.com/RuolinZheng08/renpy-chess/blob/master/gif-demo/controls.gif" alt="Flip Board" width=600>

#### Promotion UI
<img src="https://github.com/RuolinZheng08/renpy-chess/blob/master/gif-demo/promotion.gif" alt="Promotion" width=600>

### Customizations for Different Difficulty Levels

The strength of the compuer player can be customized by setting the `depth` parameter between the range of 1 and 20, with a larger number indicating more strength. See [Stockfish depth to ELO conversion](https://chess.stackexchange.com/a/8125).

### Customizations for Different Screen Sizes, Colors, Styles, and Audios

Override the defaults in `chess_displayable.rpy` and replace the default chess piece and chess board images, or, audio files in `00-chess-engine/images` and `00-chess-engine/audio`.

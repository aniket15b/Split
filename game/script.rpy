# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("ChessMaster")
define pawn = Character("Pawn Star")
define bishop = Character("Bitchin Bishop")
define knight = Character("Knight to meet you")
define rook = Character("Bookie Rook")
define queen = Character("Queen Bee")
define king = Character("King is Bling")

# The game starts here.

label start:
    scene bg room
    e "Welcome to Split!"
    $ fen = STARTING_FEN
    menu:
        "Please select the game mode."

        "Player vs. Player":
            $ player_color = None # None for Player vs. Player
            $ movetime = None
            $ depth = None

        "Player vs. Computer":
            $ movetime = 2000

            menu:
                "Please select a difficulty level"

                "Easy":
                    $ depth = 2

                "Medium":
                    $ depth = 6

                "Hard":
                    $ depth = 12

            menu:
                "Please select Player color"

                "White":
                    $ player_color = WHITE # this constant is defined in chess_displayable.rpy 

                "Black":
                    # board view flipped so that the player's color is at the bottom of the screen
                    $ player_color = BLACK
        
        "How to Play Chess":
            jump how_to_play

    window hide
    $ quick_menu = False

    # avoid rolling back and losing chess game state
    $ renpy.block_rollback()

    call screen chess(fen, player_color, movetime, depth)

    # avoid rolling back and entering the chess game again
    $ renpy.block_rollback()

    # restore rollback from this point on
    $ renpy.checkpoint()

    $ quick_menu = True
    window show

    if _return == DRAW:
        e "The game ended in a draw."
    else: # RESIGN or CHECKMATE
        $ winner = "White" if _return == WHITE else "Black"
        e "The winner is [winner]."
        if player_color is not None: # PvC
            if _return == player_color:
                e "Congratulations, player!"
            else:
                e "Better luck next time, player."

    return

label how_to_play:
    scene bg room
    window hide
    $ quick_menu = False

    show pawn moves:
        xalign 0.25
        yalign 0.5
    show pawn attacks as pawn_attacks:
        xalign 0.75
        yalign 0.5
    pawn "Unlike the other pieces, pawns cannot move backwards. \n\
        Normally a pawn moves by advancing a single square, but the first time a pawn moves, it has the option of advancing two squares. \n"
    pawn "Pawns may not use the initial two - square advance to jump over an occupied square, or to capture. \n\
        Any piece immediately in front of a pawn, friend or foe, blocks its advance. \n"
    pawn "Unlike other pieces, the pawn does not capture in the same direction that it moves. A pawn captures diagonally forward one square to the left or right."
    pawn "A pawn is worth 1 point of material."

    scene bg room
    window hide
    $ quick_menu = False

    show bishop moves:
        xalign 0.25
        yalign 0.5
    show bishop blocked as bishop_blocked:
        xalign 0.75
        yalign 0.5
    bishop "The bishop has no restrictions in distance for each move, but is limited to diagonal movement. Bishops, like all other pieces except the knight, cannot jump over other pieces."
    bishop "A bishop captures by occupying the square on which an enemy piece sits."
    bishop "As a consequence of its diagonal movement, each bishop always remains on either the white or black squares, and so it is also common to refer to them as light-squared or dark-squared bishops."
    bishop "A bishop is worth 3 points of material."

    scene bg room
    window hide
    $ quick_menu = False

    show knight moves:
        xalign 0.25
        yalign 0.5
    show knight jumps as knight_jumps:
        xalign 0.75
        yalign 0.5
    knight "Compared to other chess pieces, the knight's movement is unique: it may move two squares vertically and one square horizontally, or two squares horizontally and one square vertically (with both forming the shape of an L)."
    knight "While moving, the knight can jump over pieces to reach its destination."
    knight "Knights capture in the same way, replacing the enemy piece on the square and removing it from the board."
    knight "A knight is worth 3 points of material."

    scene bg room
    window hide
    $ quick_menu = False

    show rook moves:
        xalign 0.25
        yalign 0.5
    show rook blocked as rook_blocked:
        xalign 0.75
        yalign 0.5
    rook "The rook moves horizontally or vertically, through any number of unoccupied squares."
    rook "As with captures by other pieces, the rook captures by occupying the square on which the enemy piece sits."
    rook "A rook is worth 5 points of material."

    scene bg room
    window hide
    $ quick_menu = False

    show queen moves:
        xalign 0.25
        yalign 0.5
    show queen blocked as queen_blocked:
        xalign 0.75
        yalign 0.5
    queen "The queen can be moved any number of unoccupied squares in a straight line vertically, horizontally, or diagonally, thus combining the moves of the rook and bishop."
    queen "The queen captures by occupying the square on which an enemy piece sits."
    queen "The queen is worth 9 points of material."

    scene bg room
    window hide
    $ quick_menu = False

    show king moves:
        xalign 0.1
        yalign 0.5
    show king blocked 1 as king_blocked_1:
        xalign 0.43
        yalign 0.5
    show king blocked 2 as king_blocked_2:
        xalign 0.76
        yalign 0.5
    king "A king can move one square in any direction (horizontally, vertically, or diagonally), unless the square is already occupied by a friendly piece, or the move would place the king in check."
    king "Opposing kings can never occupy adjacent squares."
    king "The king the most important piece on the board."

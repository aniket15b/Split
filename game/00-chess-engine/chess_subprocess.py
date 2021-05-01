import os
import sys
import time
import subprocess

import_dir = sys.argv[1]
sys.path.append(import_dir)

# THIS_PATH = '00-chess-engine/'
# import_dir = os.path.join(r'C:\renpy-7.4.4-sdk\renpy-chess/game', THIS_PATH, 'python-packages')

# https://python-chess.readthedocs.io/en/v0.23.10/
import chess
import chess.uci
from chess.uci import Score

def main():
    
    chess_engine = ChessEngine()

    while True:
        line = raw_input()
        # line = input()
        # some split token corresponding to that in chess_displayable.rpy
        args = line.split('#')

        # temp = args[0]
        # args = ['fen', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', '\n']
        # chess_engine.init_board(args)
        # args = ['stockfish', u'C:\\renpy-7.4.4-sdk\\renpy-chess\\game\\00-chess-engine\\bin\\Stockfish\\stockfish_20011801_x64.exe', u'True', u'1000', u'2', u'\n']
        # chess_engine.init_stockfish(args)

        # args = [temp]

        if not args:
            continue   
        if args[0] == 'quit':
            break

        elif args[0] == 'fen':
            chess_engine.init_board(args)
        elif args[0] == 'stockfish':
            chess_engine.init_stockfish(args)
        elif args[0] == 'maiachess':
            chess_engine.init_maiachess(args)

        elif args[0] == 'stockfish_move':
            chess_engine.get_stockfish_move()
        elif args[0] == 'maiachess_move':
            chess_engine.get_maiachess_move()
        
        elif args[0] == 'game_status':
            chess_engine.get_game_status()
        elif args[0] == 'game_score':
            chess_engine.get_game_score()
        elif args[0] == 'game_eval':
            chess_engine.get_game_eval()
        elif args[0] == 'piece_at':
            chess_engine.get_piece_at(args)
        elif args[0] == 'is_capture':
            chess_engine.get_is_capture(args)
        elif args[0] == 'legal_moves':
            chess_engine.get_legal_moves()
        elif args[0] == 'push_move':
            chess_engine.push_move(args)
        elif args[0] == 'pop_move':
            chess_engine.pop_move()

        sys.stdout.flush()


class ChessEngine():

    def __init__(self):
        # enum game_status as defined in chess_displayable.rpy
        self.INCHECK = 1
        self.THREEFOLD = 2
        self.FIFTYMOVES = 3
        self.DRAW = 4
        self.CHECKMATE = 5
        self.STALEMATE = 6

        self.board = None # the chess board object
        self.stockfish = None # chess AI engine
        self.stockfish_movetime = None
        self.stockfish_depth = None

    def init_board(self, args):
        fen = args[1]
        self.board = chess.Board(fen=fen)

    def init_stockfish(self, args):
        stockfish_path = args[1]
        is_os_windows = eval(args[2])
        self.stockfish_movetime = int(args[3])
        self.stockfish_depth = int(args[4])

        # stop stockfish from opening up shell on windows
        # https://stackoverflow.com/a/63538680
        startupinfo = None
        if is_os_windows:      
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW

        self.stockfish = chess.uci.popen_engine(stockfish_path, startupinfo=startupinfo)
        self.stockfish.uci()

        self.info_handler = chess.uci.InfoHandler()
        self.stockfish.info_handlers.append(self.info_handler)

        self.stockfish.position(self.board)
    
    def init_maiachess(self, args):
        maiachess_path = args[1]
        is_os_windows = eval(args[2])
        self.maiachess_movetime = int(args[3])
        self.maiachess_depth = int(args[4])

        startupinfo = None
        if is_os_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW

        self.maiachess = chess.uci.popen_engine(maiachess_path, startupinfo=startupinfo)
        self.maiachess.uci()
        self.maiachess.position(self.board)

    def get_piece_at(self, args):
        file_idx, rank_idx = int(args[1]), int(args[2])
        piece = self.board.piece_at(chess.square(file_idx, rank_idx))
        if piece:
            print(piece.symbol())
        else:
            print('None')

    def get_is_capture(self, args):
        move_uci = args[1]
        move = chess.Move.from_uci(move_uci)
        print(self.board.is_capture(move))

    def get_game_status(self):
        if self.board.is_checkmate():
            print(self.CHECKMATE)
            return
        if self.board.is_stalemate():
            print(self.STALEMATE)
            return
        if self.board.can_claim_threefold_repetition():
            print(self.THREEFOLD)
            return
        if self.board.can_claim_fifty_moves():
            print(self.FIFTYMOVES)
            return
        if self.board.is_check():
            print(self.INCHECK)
            return
        print('-1')  # no change to game_status
        
    def get_game_score(self):
        v = dict(zip('pbnrqPBNRQ',[1,3,3,5,9]*2))
        print(sum(v.get(c,0)*(-1)**(c>'Z')for c in self.board.board_fen()))
    
    def get_game_eval(self):
        with self.info_handler:
            s = self.info_handler.info["score"].get(1, Score(cp=0, mate=None))
            if (s.cp == None):
                print("Mate in")
                print(s.mate)
            else:
                print("Evaluation")
                print(s.cp)
       
    def get_stockfish_move(self):
        self.stockfish.position(self.board)
        move = self.stockfish.go(movetime=self.stockfish_movetime, depth=self.stockfish_depth)
        move = move.bestmove
        print(move.uci())

    def get_maiachess_move(self):
        self.maiachess.position(self.board)
        move = self.maiachess.go(movetime=self.maiachess_movetime, depth=self.maiachess_depth)
        move = move.bestmove
        print("---***---***---")
        print(move.uci())

    def get_legal_moves(self):
        print('#'.join([move.uci() for move in self.board.legal_moves]))

    def push_move(self, args):
        move_uci = args[1]
        move = chess.Move.from_uci(move_uci)
        self.board.push(move)
        print(self.board.turn)

    def pop_move(self):
        # this should not raise an IndexError as the logic has been handled by the caller
        self.board.pop()
        print(self.board.turn)

if __name__ == '__main__':
    main()
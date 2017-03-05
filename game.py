import chess
import chess.svg
from player import Player
import random
#import cairosvg

class Game:
    def __init__(self, challenger, challengee):
        self.board = chess.Board()
        rand = random.randrange(0,2)
        if rand == 0:
            self.white = Player('white', challenger)
            self.black = Player('black', challengee)
        else:
            self.white = Player('white', challengee)
            self.black = Player('black', challenger)
        self.white.turn = True;
        
        
if __name__ == "__main__":
    chess1 = chess.Board()
    chess1.push_san('e4')
    cairosvg.svg2png(chess.svg.board(chess1), '/tmp/output.png')
    chess2 = chess.Board()
    #chess2.svg.board(chess2)
    print(chess1)
    print(chess2)
    

        

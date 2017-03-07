import chess
import chess.svg
from player import Player
import random
import cairo
import cairosvg

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
    def Get_Picture(self, color):
        flipped = color == "black"
        svg_data = chess.svg.board(self.board, flipped = flipped)
        cairosvg.svg2png(bytestring=svg_data, write_to = "output.png")
        
        
if __name__ == "__main__":
    chess1 = chess.Board()
    chess1.push_san('e4')
    svg_data = chess.svg.board(chess1, coordinates = False, flipped = False, style = chess.svg.DEFAULT_STYLE)
    cairosvg.svg2png(bytestring=svg_data, write_to="output2.png")
    chess2 = chess.Board()
    #chess2.svg.board(chess2)
    print(chess1)
    print(chess2)
    

        

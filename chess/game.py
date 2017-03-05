from board import Board
from player import Player
import random

#player(player, username)

class game:
    def __init__(self, challenger, challengee):
        self.board = Board()
        rand = random.randrange(0,2)
        if rand == 0:
            self.player1 = Player('white', challenger)
            self.player2 = Player('black', challengee)
        else:
            self.player1 = Player('white', challengee)
            self.player2 = Player('black', challenger)
    def print(self):
        a.player1.print()
        a.player2.print()
        a.board.print()
    def white_move(self, move):
         
    def black_move(self, move):
        

if __name__ == '__main__':
    a = game('adarsh', 'tz')
    a.print()
    
        
        
        

import numpy

WHITEPIECES = ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
BLACKPIECES = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']

class Board:
    def __init__(self):
        self.Board = numpy.chararray((8,8), itemsize = 2)
        self.Board[:] = '0'
        self.column_dictionary = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        counter = 0
        for row in self.Board:
            columncounter = 0 
            for column in row: 
                if (counter == 0):
                    self.Board[counter][columncounter] = WHITEPIECES[columncounter]
                elif (counter == 7):
                    self.Board[counter][columncounter] = BLACKPIECES[columncounter]
                elif (counter == 1):
                    self.Board[counter][columncounter] = 'WP'
                elif (counter == 6):
                    self.Board[counter][columncounter] = 'BP'
                columncounter = columncounter + 1
            counter = counter + 1
    def print(self):
        print(self.Board) 
    #position should be the last two string characters of a move    
    def isEmpty(self, position):
        column = self.column_dictionary(position[0])    
        row = position[1]
        return self.Board[row][column] == 0
    def white_move(self, move):
        if len(move) == 2:
            #pawn
            column = move[0]
            row = move[1]
            pawn = self.Board[row][column]
            pawn.check_move
        if len(move) == 3:
            #piece
            column = move[1]
            row = move[2]
            piece = self.board[row][column]
            piece.check_move
        
            
            
    
if __name__ == "__main__":
    a = Board()
    a.print()

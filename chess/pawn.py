from piece import Piece

class Pawn(Piece):
    def __init__(self, position, color):
        self.position = position
        self.name = 'Pawn' 
        self.captured = False
        self.color = color
        
    def check_move(self, move, board):
        d = board.column_dictionary
        if len(move) == 2:
            if move[0] != position[0]:
                return false
            elif int(move[1]) == int(self.position[2]) + 1 and board.isEmpty(move[0:2])
                board.Board(a
                
    def set_position(self, newposition):
        self.position = newposition
    def set_name(self, name):
        self.name = name
    def set_captured(self):
        self.captured = True

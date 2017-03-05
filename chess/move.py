
class Move:
    def __init__(self, move):
        if len(move) == 2:
            self.column = move[0]
            self.row = move[1]
        elif len(move) == 3:
            self.column = move[1]
            self.row = move[2]
            #if the piece is a rook/knight/bishop
        elif len(move) == 4:
            if move[0].istitle():
                #capture with piece
                if move[1].isalpha():
                    #move with correct piece
            elif not move[0].istitle():
                #capture with pawn
             

class Piece
    def __init__(self): 
       self.position = None
       self.name = None
    def movement(self):
        raise NotImplementedError('subclasses must override movement')
    def set_position(self, newposition):
        raise NotImplementedError('subclasses must ovveride set_position')
    def set_name(self):
        raise NotImplementedError('subclasses must ovveride set_name')
    def set_captured(self):
        raise NotImplementedError('subclasses must ovveride set_captured')

        
        
   

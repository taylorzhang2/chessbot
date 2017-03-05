#player class
#constructor: player = white or black
class Player:
    def __init__(self, color, username):
       self.color = color
       self.username = username
       self.turn = False
    def move(self, move):
        return
    def print(self):
        print(self.player)
        print(self.username)
        
if __name__ == "__main__":
    a = Player('white', 'adarsh')
    a.print()

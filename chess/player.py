#player class
#constructor: player = white or black
class Player:
    def __init__(self, player, username, id):
        self.player = player
        self.username = username
#       self.mention = self.username.mention

        self.id = id

    def move(self, move):
        return
    def print(self):
        print(self.player)
        print(self.username)

if __name__ == "__main__":
    a = Player('white', 'adarsh')
    a.print()

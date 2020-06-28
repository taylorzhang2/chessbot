from discord.ext import commands
import discord
import chess
import chess.svg
import random
import cairo
import cairosvg
import logging


logging.basicConfig(level=logging.DEBUG)

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

class Game(commands.Cog):
    def __init__(self, bot):
        self.board = chess.Board()
        self.white = ''
        self.black = ''
        self.bot = bot
    def Reset(self):
        self.white = ''
        self.black = ''
        self.board = chess.Board()
    def Get_Picture(self, color):
        flipped = color == "black"
        svg_data = chess.svg.board(self.board, flipped = flipped)
        cairosvg.svg2png(bytestring=svg_data, write_to = "output.png")
    def Take_Turn(self):
        self.white.turn = not self.white.turn
        self.black.turn = not self.black.turn

    @commands.command(name='coolbot')
    async def cool_bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('This bot is cool. :)')

    @commands.command()
    async def test(self, ctx):
        print("////")
        await ctx.send('test test')
    @commands.command()
    async def currentposition(self, color):
        await ctx.send('Current board position:')
        Get_Picture(color)
    @commands.command(pass_context=True)
    async def playchess(self, ctx, name = ''):
        if self.white != '' and self.black != '':
            return await ctx.send('There is already a game being played on this server')
        if len(ctx.message.mentions) == 0:
            return await ctx.send('You must mention another player to start a game.')
        if len(ctx.message.mentions) > 1:
            return await ctx.send('You are mentioning too many people')
        if ctx.message.mentions[0] == ctx.message.author:
            return await ctx.send('You cannot play against yourself!')

        author = ctx.message.author
        opponent = ctx.message.mentions[0]
        rand = random.randrange(0,2)
        self.white = Player('white', author) if rand == 0 else Player('white', opponent.name + "#" +  opponent.discriminator)
        self.black = Player('black', author) if rand != 0 else Player('black', opponent.name + "#" + opponent.discriminator)
        self.white.turn = True
        self.Get_Picture('white')
        await self.bot.send_file(ctx.message.channel, fp = 'output.png')
        await self.bot.send_message(ctx.message.channel, 'Your move, {}'.format(self.white.username))
    @commands.command(pass_context=True)
    async def move(self, ctx, move = ''):
        if self.white == '' and self.black == '':
            ctx.send('There is no active game available')
        if move == '':
            ctx.send('You must supply a move')
        player = self.white if self.white.turn == True else self.black
        logging.warning(player.username)
        logging.warning(ctx.message.author)
        if str(ctx.message.author) != str(player.username):
            return await self.bot.send_message(ctx.message.channel, 'It is not your turn, {}'.format(ctx.message.author))
        else:
            try:
                self.board.push_san(move)
                self.Take_Turn()
                color = "white" if player != self.white else "black"
                nextuser = self.white.username if player != self.white else self.black.username
                self.Get_Picture(color)
                if self.board.is_game_over() == True:
                    await self.bot.send_file(ctx.message.channel, fp = 'output.png')
                    await self.bot.send_message(ctx.message.channel, 'Game over. {}'.format(self.board.result()))
                    self.Reset()
                else:
                    await self.bot.send_file(ctx.message.channel, fp = 'output.png')
                    await self.bot.send_message(ctx.message.channel, 'Your move, {}'.format(nextuser))
            except ValueError:
                await self.bot.send_message(ctx.message.channel, '{} is an illegal move, {}'.format(move, ctx.message.author))

def setup(bot):
    bot.add_cog(Game(bot))

"""
if __name__ == "__main__":
    chess1 = chess.Board()
    chess1.push_san('e4')
    svg_data = chess.svg.board(chess1, coordinates = False, flipped = False, style = chess.svg.DEFAULT_STYLE)
    cairosvg.svg2png(bytestring=svg_data, write_to="output2.png")
    chess2 = chess.Board()
    #chess2.svg.board(chess2)
    print(chess1)
    print(chess2)
"""

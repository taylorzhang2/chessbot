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
#       self.mention = self.username.mention
    def move(self, move):
        return
    def print(self):
        print(self.player)
        print(self.username)

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
            await ctx.message.delete()
            return await ctx.send('There is already a game being played on this server')
        if len(ctx.message.mentions) == 0:
            await ctx.message.delete()
            return await ctx.send('You must mention another player to start a game.')
        if len(ctx.message.mentions) > 1:
            await ctx.message.delete()
            return await ctx.send('You are mentioning too many people')
        if ctx.message.mentions[0] == ctx.message.author:
            await ctx.message.delete()
            return await ctx.send('You cannot play against yourself!')
        author = ctx.message.author
#        self.author_player = ctx.message.author
        opponent = ctx.message.mentions[0]
#        self.opponent_player = ctx.message.mentions[0]
        rand = 0 #random.randrange(0,2)
        self.white = Player('white', author) if rand == 0 else Player('white', opponent.name + "#" +  opponent.discriminator)
        self.black = Player('black', author) if rand != 0 else Player('black', opponent.name + "#" + opponent.discriminator)
        self.white.turn = True
        self.Get_Picture('white')
        file=discord.File('./output.png', filename='output.png')
        embed=discord.Embed()
        embed.set_image(url="attachment://output.png")
        await ctx.message.channel.send(content='Your move, {}'.format(self.white.username), embed=embed)
#       await ctx.message.channel.send('Your move, {}'.format(self.white.username))
    @commands.command(pass_context=True)
    async def move(self, ctx, move = ''):
        if self.white == '' and self.black == '':
            await ctx.message.delete()
            ctx.send('There is no active game available', delete_after=5)
        if move == '':
            await ctx.message.delete()
            ctx.send('You must supply a move', delete_after=5)
        player = self.white if self.white.turn == True else self.black
        logging.warning(player.username)
        logging.warning(ctx.message.author)
        if str(ctx.message.author) != str(player.username):
            return await ctx.message.channel.send('It is not your turn, {}'.format(ctx.message.author), delete_after=5)
            await ctx.message.delete()
        elif move == 'resign':
#            await ctx.message.channel.send('', file=discord.File('output.png', 'output.png'))
#            await ctx.message.channel.send('Game over. {} resigned.'.format(ctx.message.author))
            file=discord.File('./output.png', filename='output.png')
            embed=discord.Embed()
            embed.set_image(url="attachment://output.png")
            await ctx.message.channel.edit(content='Game over. {} resigned.'.format(ctx.message.author), embed=embed)
            await ctx.message.delete()
            self.Reset()
        else:
            try:
                self.board.push_san(move)
                self.Take_Turn()
                color = "white" if player != self.white else "black"
                nextuser = self.white.username if player != self.white else self.black.username
                self.Get_Picture(color)
                if self.board.is_game_over() == True:
#                    await ctx.message.channel.send('', file=discord.File('output.png', 'output.png'))
#                    await ctx.message.channel.send('Game over. {}'.format(self.board.result()))
                    file=discord.File('./output.png', filename='output.png')
                    embed=discord.Embed()
                    embed.set_image(url="attachment://output.png")
                    await ctx.message.channel.edit(content='Game over. {}'.format(self.board.result()), embed=embed)
                    self.Reset()
                else:
#                    await ctx.message.channel.send('', file=discord.File('output.png', 'output.png'))
#                    await ctx.message.channel.send('Your move, {}'.format(nextuser))
                    file=discord.File('./output.png', filename='output.png')
                    embed=discord.Embed()
                    embed.set_image(url="attachment://output.png")
                    await ctx.message.channel.edit(content='Your move, {}'.format(nextuser), embed=embed)
            except ValueError:
                await ctx.message.channel.send('{} is an illegal move, {}'.format(move, ctx.message.author), delete_after=5)

def setup(bot):
    bot.add_cog(Game(bot))

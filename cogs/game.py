from discord.ext import commands
import discord
import chess
import chess.svg
import random
import cairo
import cairosvg
import logging
import asyncio
import time
import threading

logging.basicConfig(level=logging.DEBUG)

class Player:
    def __init__(self, color, username, id):
        self.color = color
        self.username = username
        self.turn = False
#       self.mention = self.username.mention

        self.id = id

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

        self.is_first_upload = True

        self.last_move = 'none'

        self.nextuser = None

        self.draw_message = None

        self.player = None

        self.opposingPlayer = None

    def Reset(self):
        self.white = ''
        self.black = ''
        self.board = chess.Board()

        self.is_first_upload = True

    def Get_Picture(self, color):
        flipped = color == "black"
        svg_data = chess.svg.board(self.board, flipped = flipped)
        cairosvg.svg2png(bytestring=svg_data, write_to = "output.png")

    def Take_Turn(self):
        self.white.turn = not self.white.turn
        self.black.turn = not self.black.turn

    async def Update_Message(self, ctx, embed_title, edit=False):
        file=discord.File('./output.png', filename='image.png')
        embed=discord.Embed()
        embed.set_image(url="attachment://image.png")
        self.burner_channel = self.bot.get_channel(727054721789198357)
        latest_image = await self.burner_channel.send(file=file, embed=embed)
        embed=discord.Embed(title=embed_title, description='Last move: ' + self.last_move)
        embed.set_image(url=latest_image.embeds[0].image.url)
        footer_text = "White: {}".format(self.white.username) + "\nBlack: {}".format(self.black.username)
        embed.set_footer(text=footer_text)
        if edit: # edit message
            await self.first_message.edit(embed=embed)
        else: # send message
            self.first_message = await ctx.message.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def test(self, ctx):
        print("////")
        await ctx.send('test test')

    @commands.command(pass_context=True)
    async def currpos(self, ctx, color):
        # await ctx.send('Current board position:')
        self.Get_Picture(color)
        await self.first_message.delete()
        embed_title = 'Your move, {}'.format(self.nextuser)
        await self.Update_Message(ctx, embed_title=embed_title)

    @commands.command(pass_context=True)
    async def play(self, ctx, name = ''):
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
        self.nextuser = author
        rand = 0 #random.randrange(0,2)
        self.white = Player('white', author, ctx.message.author.id) if rand == 0 else Player('white', opponent.name + "#" +  opponent.discriminator, ctx.message.mentions[0].id)
        self.black = Player('black', author, ctx.message.author.id) if rand != 0 else Player('black', opponent.name + "#" + opponent.discriminator, ctx.message.mentions[0].id)
        self.white.turn = True
        self.Get_Picture('white')
        # user_id_to_mention = str(self.white.id)
        # other_user_id_to_mention = str(self.black.id)
        # logging.warning("user_to_mention: <@" + str(user_id_to_mention) + '>')
        # user_to_mention = self.bot.get_user(int(user_id_to_mention))
        #embed.add_field(name="Current player to move:", value="<@" + str(user_id_to_mention) + '>')
        #footer_text = "White: <@" + str(user_id_to_mention) + ">\nBlack: <@" + str(other_user_id_to_mention) + ">"
        embed_title = 'Your move, {}'.format(self.white.username)
        await self.Update_Message(ctx, embed_title=embed_title)

    @commands.command(pass_context=True)
    async def move(self, ctx, move = ''):
        await ctx.message.delete()
        if self.white == '' and self.black == '':
            ctx.send('There is no active game available', delete_after=5)
        if move == '':
            ctx.send('You must supply a move', delete_after=5)
        self.player = self.white if self.white.turn == True else self.black
        self.opposingPlayer = self.black if self.white.turn == True else self.white
        logging.warning("Opposing Player: " + str(self.opposingPlayer.username))
        logging.warning("Player: " + str(self.player.username))
        logging.warning("Message Author: " + str(ctx.message.author))
        player_is_opposing_player = str(ctx.message.author) == str(self.bot.get_user(int(self.opposingPlayer.id)))
        player_is_current_player = str(ctx.message.author) == str(self.player.username)


        if move == 'resign':
            logging.warning("Move: " + str(move))
            logging.warning("ctx.message.author: " + str(ctx.message.author))
            logging.warning("opposingPlayer.id: " + str(self.opposingPlayer.id))
            logging.warning("player.username: " + str(self.player.username))
        if str(ctx.message.author) != str(self.player.username) and move != 'resign':
            return await ctx.message.channel.send('It is not your turn, {}'.format(ctx.message.author), delete_after=5)
        if move == 'draw':
            if player_is_current_player: # it's the turn of the person offering the draw
                logging.warning("player_is_current_player: " + str(player_is_current_player))
                self.draw_message = await ctx.send("<@" + str(self.opposingPlayer.id) + ">, " + str(ctx.message.author) + ' has offered a draw. Do you accept?', delete_after=20)
                await self.draw_message.add_reaction('✅')
                await self.draw_message.add_reaction('❌')
                reacted = False
        elif move == 'resign' and (player_is_opposing_player or player_is_current_player):
            if self.is_first_upload:
                await self.first_message.delete()
                embed_title = 'Game over. {} resigned.'.format(ctx.message.author)
                await self.Update_Message(ctx, embed_title=embed_title)
                self.Reset()
            else:
                embed_title = 'Game over. {} resigned.'.format(ctx.message.author)
                await self.Update_Message(ctx, embed_title=embed_title, edit=True)
                self.Reset()
        #...

                """
                async def mytimer2():
                    if not reacted:
                        await ctx.message.channel.send('Draw offer timed out.', delete_after=5)
                    my_timer = threading.Timer(11.0, mytimer2)
                    my_timer.start()
                time.sleep(5)
                async def check_mark_react(message):
                    logging.warning("in check_mark_react. opposingPlayer is below... ")
                    logging.warning(opposingPlayer.username)
                    check_react_from_opposing_player = False
                    for i in message.reactions:
                        logging.warning(i)
                        users = await i.users().flatten()
                        logging.warning(users)
                        if str(i) == '✅' and self.bot.get_user(int(opposingPlayer.id)) in users:
                            check_react_from_opposing_player = True
                    return check_react_from_opposing_player
                    # return user == self.bot.get_user(int(opposingPlayer.id)) and str(reaction.emoji) == '✅'
                async def x_react(message):
                    logging.warning("in x_mark_react. opposingPlayer is below... ")
                    logging.warning(opposingPlayer.username)
                    check_react_from_opposing_player = False
                    for i in message.reactions:
                        users = await i.users().flatten()
                        if str(i) == '❌' and self.bot.get_user(int(opposingPlayer.id)) in users:
                            check_react_from_opposing_player = True
                    return check_react_from_opposing_player
                    # return user == self.bot.get_user(int(opposingPlayer.id)) and str(reaction.emoji) == '❌'
                async def check_for_reactions():
                    logging.warning("Checking for reactions...")
                    if await check_mark_react(draw_message):
                        reacted = True
                        embed_title = 'Game over. ' + str(ctx.message.author) + ' and ' + str(opposingPlayer.username) + ' have agreed to a draw.'
                        await self.Update_Message(ctx, embed_title=embed_title, edit=True)
                        self.Reset()
                    if await x_react(draw_message):
                        reacted = True
                        await ctx.message.channel.send('Draw offer declined.', delete_after=10)
                await check_for_reactions()
                async def check_mark_react2(message):
                    logging.warning("in check_mark_react. opposingPlayer is below... ")
                    logging.warning(opposingPlayer.username)
                    check_react_from_opposing_player = False
                    for i in message.reactions:
                        logging.warning(i)
                        users = await i.users().flatten()
                        logging.warning(users)
                        if str(i) == '✅' and self.bot.get_user(int(opposingPlayer.id)) in users:
                            check_react_from_opposing_player = True
                    return check_react_from_opposing_player
                    # return user == self.bot.get_user(int(opposingPlayer.id)) and str(reaction.emoji) == '✅'
                async def x_react2(message):
                    logging.warning("in x_mark_react. opposingPlayer is below... ")
                    logging.warning(opposingPlayer.username)
                    check_react_from_opposing_player = False
                    for i in message.reactions:
                        users = await i.users().flatten()
                        if str(i) == '❌' and self.bot.get_user(int(opposingPlayer.id)) in users:
                            check_react_from_opposing_player = True
                    return check_react_from_opposing_player
                    # return user == self.bot.get_user(int(opposingPlayer.id)) and str(reaction.emoji) == '❌'
                async def check_for_reactions2():
                    logging.warning("Checking for reactions...")
                    if await check_mark_react2(draw_message):
                        reacted = True
                        embed_title = 'Game over. ' + str(ctx.message.author) + ' and ' + str(opposingPlayer.username) + ' have agreed to a draw.'
                        await self.Update_Message(ctx, embed_title=embed_title, edit=True)
                        self.Reset()
                    if await x_react2(draw_message):
                        reacted = True
                        await ctx.message.channel.send('Draw offer declined.', delete_after=10)
                time.sleep(5)
                await check_for_reactions2()
                """

                # if opponent reacts with check:
                #   draw code goes here...
                # else:
                #   tell opponent to suck it
        else:
            try:
                self.last_move = move
                self.board.push_san(move)
                self.Take_Turn()
                color = "white" if player != self.white else "black"
                self.nextuser = self.white.username if player != self.white else self.black.username
                self.Get_Picture(color)
                if self.board.is_game_over() == True:
                    embed_title = 'Game over. {}'.format(self.board.result())
                    await self.Update_Message(ctx, embed_title=embed_title, edit=True)
                    self.Reset()
                else:
                    if self.is_first_upload:
                        await self.first_message.delete()
                        self.is_first_upload = False
                        embed_title = 'Your move, {}'.format(self.nextuser)
                        await self.Update_Message(ctx, embed_title=embed_title)
                    else:
                        embed_title = 'Your move, {}'.format(self.nextuser)
                        await self.Update_Message(ctx, embed_title=embed_title, edit=True)
            except ValueError:
                await ctx.message.channel.send('{} is an illegal move, {}'.format(move, ctx.message.author), delete_after=5)

def setup(bot):
    bot.add_cog(Game(bot))

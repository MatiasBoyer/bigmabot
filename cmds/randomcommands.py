import resources.dsbot_extensions as ext
import asyncio
import discord
from playsound import playsound
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions
from cleverbot_free.cbapi import CleverBot
from datetime import datetime


class RandomCommands(commands.Cog):

    cbenabled = False
    cb = CleverBot()
    bot = None

    def __init__(self, _bot, cbenabled):
        self.cb = CleverBot()
        self.bot = _bot
        self.cbenabled = cbenabled
        if cbenabled == True:
            self.cb.init()

    @commands.command(name="cleverbot.ask")
    async def cleverbot_ask(self, ctx, *msg):
        if self.cbenabled == False:
            await ctx.send("bot has this command disabled!")
            return

        await ctx.send("Thinking... ⏳")
        response = self.cb.getResponse(' '.join(msg))
        await ctx.send(f"cleverbot says: {response}")
        # cb_response = cb.single_exchange(msg)

    @ commands.command(name="gitlink")
    async def gitlink(self, ctx):
        await ctx.send("https://github.com/MatiasBoyer/bigmabot")

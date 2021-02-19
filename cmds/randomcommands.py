import resources.dsbot_extensions as ext
import asyncio
import discord
from playsound import playsound
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions
from cleverbot_free.cbapi import CleverBot


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

    @commands.command(name="cleverbot.ask", brief="DISABLED!")
    async def cleverbot_ask(self, ctx, msg):
        if self.cbenabled == False:
            await ctx.send("bot has this command disabled!")
            return
        await ctx.send(self.cb.getResponse(f"cleverbot says: {msg}"))
        #cb_response = cb.single_exchange(msg)

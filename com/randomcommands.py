import dsbot_extensions as ext
import asyncio
import discord
from playsound import playsound
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions
from cleverbot_free.cbapi import CleverBot


class RandomCommands(commands.Cog):

    cb = CleverBot()
    bot = None

    def __init__(self, _bot):
        self.cb = CleverBot()
        self.cb.init()
        self.bot = _bot

    @commands.command(name="sendtobigma")
    async def sendtobigma(self, ctx, msg):
        u = await self.bot.fetch_user(301493792366657537)
        await u.send(msg)
        playsound("./uploads/alarm.mp3")
        await ctx.send(f"Ya le mande el dm a bigma y le puse un sonido en la pc.")

    @commands.command(name="cleverbot.ask", brief="DISABLED!")
    async def cleverbot_ask(self, ctx, msg):
        await ctx.send("Command disabled")
        return
        await ctx.send(self.cb.getResponse(f"cleverbot says: {msg}"))
        #cb_response = cb.single_exchange(msg)

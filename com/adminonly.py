from asyncio.subprocess import STDOUT
import discord
import emojilist
from discord import client
import dsbot_extensions as ext
from discord.ext import commands
#from discord.ext.commands import bot
from discord.ext.commands.core import has_permissions


class AdminOnly(commands.Cog):
    # sendtochannel XXXXXXXX "MESSAGE"
    bot = None
    answerlist = None

    def __init__(self, _bot, _answerlist):
        super().__init__()
        self.bot = _bot
        self.answerlist = _answerlist

    @commands.command(name="send.tochannel")
    @has_permissions(manage_roles=True)
    async def sendtochannel(self, ctx, id, msg):
        # await ctx.send(id)
        msg = emojilist.replaceEmojiInString(msg)
        channel = await self.bot.fetch_channel(channel_id=int(id))
        await channel.send(msg)

    @ commands.command(name="send.touser")  # sendtochannel XXXXXXXX "MESSAGE"
    @ has_permissions(manage_roles=True)
    async def sendtouser(self, ctx, id, msg):
        msg = emojilist.replaceEmojiInString(msg)
        u = await self.bot.fetch_user(user_id=int(id))
        await u.send(msg)

    @ commands.command(name="json.reload")
    @ has_permissions(manage_roles=True)
    async def jsonreload(self, ctx):
        ext.LOADJSON(self.answerlist)
        await ctx.send("LOADJSON() called!")

    @ commands.command(name="json.save")
    @ has_permissions(manage_roles=True)
    async def jsonsave(self, ctx):
        ext.SAVEJSON(self.answerlist)
        await ctx.send("SAVEJSON() called!")

    @ commands.command()
    @ has_permissions(manage_roles=True)
    async def evaluate(self, ctx, msg):
        eval_result = eval(msg)
        await ctx.send(eval_result)

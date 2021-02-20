from asyncio.subprocess import STDOUT
from typing import final
import discord
import resources.emojilist as emojilist
from discord import client
import resources.dsbot_extensions as ext
from discord.ext import commands
#from discord.ext.commands import bot
from discord.ext.commands.core import has_permissions
import resources.guildsave as guildsave


class AdminOnly(commands.Cog):
    # sendtochannel XXXXXXXX "MESSAGE"
    bot = None

    def __init__(self, _bot):
        super().__init__()
        self.bot = _bot

    @commands.command(name="send.tochannel")
    @has_permissions(manage_roles=True)
    async def sendtochannel(self, ctx, id, *msg):
        # await ctx.send(id)
        m = emojilist.replaceEmojiInString(' '.join(msg))
        if '<' in id:
            id = id[2:]
            id = id[:len(id) - 1]

        channel = await self.bot.fetch_channel(channel_id=int(id))
        await channel.send(m)

    @ commands.command(name="send.touser")  # sendtochannel XXXXXXXX "MESSAGE"
    @ has_permissions(manage_roles=True)
    async def sendtouser(self, ctx, id, *msg):
        m = emojilist.replaceEmojiInString(' '.join(msg))

        if '<' in id:
            id = id[3:]
            id = id[:len(id) - 1]

        u = await self.bot.fetch_user(user_id=int(id))
        await u.send(m)

    @commands.command(name="conf.list")
    @has_permissions(administrator=True)
    async def conf_list(self, ctx):
        guildconf = await guildsave.returnGuildJson(ctx, str(ctx.message.guild.id))

        finaltext = ""
        confdic = guildconf["userConfig"]

        finaltext += "**LIST OF CONFIGURABLE PARAMETERS**\n"
        finaltext += "Category name: **SWITCHES**:\n"
        for x in confdic["switches"]:
            value = confdic["switches"][x]
            finaltext += f"- {x} -> _{value}_\n"

        await ctx.send(f"{finaltext}")

    @commands.command(name="conf.setparameter")
    @has_permissions(administrator=True)
    async def conf_setparameter(self, ctx, parameterName, parameterCategory, parameterValue):
        guildconf = await guildsave.returnGuildJson(ctx, str(ctx.message.guild.id))

        try:
            parameterName = parameterName.lower()
            parameterCategory = parameterCategory.lower()
            changedParameter = False

            if parameterCategory == "switches":
                guildconf["userConfig"][parameterCategory][parameterName] = (
                    parameterValue.lower() == "true")
                changedParameter = True

            if changedParameter == False:
                await ctx.send("Error changing parameters!")
                return

            guildsave.saveDataToJson(ctx.message.guild.id, guildconf)
            await ctx.send("Changed parameter!")
        except:
            await ctx.send("Error changing parameters!")

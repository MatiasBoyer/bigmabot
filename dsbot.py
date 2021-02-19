# region IMPORTS
import discord
import traceback
import time
import json
import resources.emojilist as emojilist
import resources.guildsave as guildsave
import configparser

from discord.ext.commands.errors import CommandNotFound
import resources.dsbot_extensions as ext
from playsound import playsound
from termcolor import colored
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions

# COMMANDS IMPORT
from cmds.rand import Rand
from cmds.randomcommands import RandomCommands
from cmds.file import File
from cmds.answers import Answers
from cmds.adminonly import AdminOnly
from cmds.images import Images
import cmds.memes as memes
# endregion

# region USEFUL VARIABLES
mediatypes = [".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".gif"]

token = ""
cbenabled = False
imgflipData = memes.imgflipData(False, "", "")
# endregion

# region BOT INITIALIZATION
bot = commands.Bot(command_prefix="$")

bot.add_cog(Rand())
bot.add_cog(AdminOnly(bot))
bot.add_cog(File())
bot.add_cog(RandomCommands(bot, cbenabled))
bot.add_cog(Answers())
bot.add_cog(Images())
bot.add_cog(memes.Memes(imgflipData))


@bot.event
async def on_ready():
    print("on_ready() called!")
    # await sendToOwner("on_ready() called!")
    await bot.change_presence(activity=discord.Streaming(name="TESTING! NO FUNCIONO", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # COMMAND HANDLING
    guildsettings = guildsave.returnGuildJson(str(message.guild.id))

    author_colored = colored((message.author), "red")
    print(f"{author_colored} -> {message.content}")
    await bot.process_commands(message)

    # RANDOM_ANSWERS TEST!
    if int(guildsettings["LastCheckTime"]) >= time.time() - guildsettings["AnswerCooldown"]:
        #print("wordchecking is on cooldown!")
        return

    if len(message.content) <= 1:
        return

    if message.content[0] == '$':
        return

    guildsettings["LastCheckTime"] = time.time()

    guildsave.saveDataToJson(str(message.guild.id), guildsettings)

    random_answers = []
    for x in guildsettings["AnswerList"]:
        a = ext.word_answering_random(
            x["NAME"], x["TYPE"], x["WORDS"], x["ANSWERS"])
        random_answers.append(a)

    for ra in random_answers:
        a = ra.checkword(message.content)
        if a != None:
            a = emojilist.replaceEmojiInString(a)

            if ra.returnType() == "TEXT":
                await message.channel.send(a.format(message.author.mention))
                return
            if ra.returnType() == "MEDIA":
                await message.channel.send(file=discord.File("./uploads/" + a))
                return
            if ra.returnType() == "TEXTNMEDIA":
                if ext.isAdmitedMediaType(mediatypes, a):
                    await message.channel.send(file=discord.File("./uploads/" + a))
                else:
                    await message.channel.send(a.format(author=message.author.mention))
                return
            if ra.returnType() == "EMOJI":
                await message.add_reaction(a)
                return


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    raise error

# endregion

# region BOT CONFIG
config = configparser.ConfigParser()
config.read("config.ini")

# IMGFLIP
imgflipData.isEnabled = config["IMGFLIP"]["Enable"] == "True"
imgflipData.username = config["IMGFLIP"]["Username"]
imgflipData.password = config["IMGFLIP"]["Password"]

# CLEVERBOT
cbenabled = config["CLEVERBOT"]["Enable"] == "True"

# TOKEN
token = config["BOTCONF"]["Token"]

# endregion

bot.run(token.strip())

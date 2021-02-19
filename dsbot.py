# region IMPORTS
import discord
import traceback
import time
import json
import emojilist
import guildsave

from discord.ext.commands.errors import CommandNotFound
import dsbot_extensions as ext
from playsound import playsound
from termcolor import colored
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions

# COMMANDS
from com.rand import Rand
from com.randomcommands import RandomCommands
from com.file import File
from com.answers import Answers
from com.adminonly import AdminOnly
from com.images import Images
from com.memes import Memes
# endregion

# region USEFUL VARIABLES
token = ""
mediatypes = [".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".gif"]
# endregion

# region SAVING/LOADING HELPERS


def LOADJSON():
    print(colored("DEPRECATED", 'red'))
    return
    # BOTCONFIG
    botconf = ext.returndatafromfile("./config/botconfig.json")
    wordcheckingcooldown = botconf["WordCheckCooldown"]

    # RANDOM_ANSWERS
    random_answers.clear()
    answerlist = ext.returndatafromfile("./config/answerlist.json")
    for x in answerlist["LIST"]:
        a = ext.word_answering_random(
            x["NAME"], x["TYPE"], x["WORDS"], x["ANSWERS"])
        random_answers.append(a)


def SAVEJSON():
    print(colored("DEPRECATED", 'red'))
    return

    # BOTCONFIG
    botconfdict = {
        "WordCheckCooldown": wordcheckingcooldown
    }
    botconfjson = json.dumps(botconfdict)
    ext.savedatatofile("./config/botconfig.json", botconfjson)

    # RANDOM_ANSWERS
    answerstojson = []
    j = "{ " + "\"LIST\": "

    for x in random_answers:
        answerstojson.append(x.toJson())
    atojson = j + ext.arrayToStrWithoutQuotationMarks(answerstojson) + "]}"
    # print(atojson)
    ext.savedatatofile("./config/answerlist.json", atojson)


# endregion

# region BOT INITIALIZATION
bot = commands.Bot(command_prefix="$")

# bot.add_cog(Rand())
# bot.add_cog(AdminOnly(bot))
# bot.add_cog(File())
# bot.add_cog(RandomCommands(bot))
bot.add_cog(Answers())
# bot.add_cog(Images())
# bot.add_cog(Memes())


async def sendToOwner(msg):
    u = await bot.fetch_user(301493792366657537)
    await u.send(msg)


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
            await sendToOwner(
                f"[!] Error! Message type '{ra.returnType()}' not recognized.")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    raise error

token = open("token", 'r').readline()
LOADJSON()

bot.run(token.strip())
# endregion

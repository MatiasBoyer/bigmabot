#region IMPORTS
from asyncio.subprocess import STDOUT
import discord, asyncio, inspect, random, sys, json, requests, os
import dsbot_extensions as ext
from playsound import playsound
from termcolor import colored
from discord import client
from discord import message
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions
from com.rand import Rand
from com.randomcommands import RandomCommands
from com.file import File
from com.answers import Answers
from com.adminonly import AdminOnly
#endregion

#region USEFUL VARIABLES
token = ""
random_answers = []
#endregion

#region SAVING/LOADING HELPERS
def LOADJSON():
    random_answers.clear()
    answerlist = ext.returndatafromfile("answerlist.json")
    for x in answerlist["LIST"]:
        a = ext.word_answering_random(x["NAME"], x["TYPE"], x["WORDS"], x["ANSWERS"])
        random_answers.append(a)

def SAVEJSON():
    answerstojson = []
    j = "{ " + "\"LIST\": "

    for x in random_answers:
        answerstojson.append(x.toJson())
    atojson = j + ext.arrayToStrWithoutQuotationMarks(answerstojson) + "]}"
    #print(atojson)
    ext.savedatatofile("answerlist.json", atojson)
#endregion

#region BOT COMMANDS
bot = commands.Bot(command_prefix = "$")

bot.add_cog(Rand())
bot.add_cog(AdminOnly())
bot.add_cog(File())
bot.add_cog(RandomCommands())
bot.add_cog(Answers(random_answers))
#endregion

#region BOT EVENTS    
async def sendToOwner(msg):
    u = await bot.fetch_user(301493792366657537)
    await u.send(msg)
@bot.event
async def on_ready():
    print("on_ready() called!")
    #await sendToOwner("on_ready() called!")
    await bot.change_presence(activity = discord.Streaming(name = "SI NO CONTESTO TU COMANDO ES PORQUE SEGURO LO PUSISTE MAL", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    ### COMMAND HANDLING
    author_colored = colored((message.author), "red")
    print (f"{author_colored} -> {message.content}")
    await bot.process_commands(message)

    ### RANDOM_ANSWERS TEST!
    if message.content[0] == '$':
        return

    for ra in random_answers:
        a = ra.checkword(message.content)
        if a != None:
            if ra.returnType() == "TEXT":
                await message.channel.send(a.format(message.author.mention))
                return
            if ra.returnType() == "MEDIA":
                await message.channel.send(file = discord.File("./uploads/" + a))
                return
            sendToOwner(f"[!] Error! Message type '{ra.returnType()}' not recognized.")
#endregion

#region BOT INITIALIZATION
token = open("token", 'r').readline()
LOADJSON()

bot.run(token.strip())
#endregion
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
#endregion

#region USEFUL VARIABLES
token = "**********"
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
class Rand(commands.Cog):
    @commands.command(name = "rand.range")  # randrange MIN MAX
    async def randrange(self, ctx, min, max):
        i = random.randrange(int(min), int(max + 1))
        await ctx.send(f"randrange -> {i}")
    
    @commands.command(name = "rand.float")
    async def randfloat(self, ctx, min, max):
        f = random.uniform(float(min), float(max))
        await ctx.send(f"randfloat -> {f}")

    @commands.command(name = "rand.setseed")
    async def randsetseed(self, ctx, seed):
        random.seed(seed)
        await ctx.send(f"random.seed('{seed}') called!")

class AdminOnly(commands.Cog):
    @commands.command(name = "send.tochannel")  # sendtochannel XXXXXXXX "MESSAGE"
    @has_permissions(manage_roles=True)
    async def sendtochannel(self, ctx, id, msg):
        channel = bot.get_channel(int(id))
        await channel.send(msg)
    
    @commands.command(name = "send.touser")  # sendtochannel XXXXXXXX "MESSAGE"
    @has_permissions(manage_roles=True)
    async def sendtouser(self, ctx, id, msg):
        u = await bot.fetch_user(int(id))
        await u.send(msg)

    @commands.command(name = "json.reload")
    @has_permissions(manage_roles=True)
    async def jsonreload(self, ctx):
        LOADJSON()
        await ctx.send("LOADJSON() called!")

    @commands.command(name = "json.save")
    @has_permissions(manage_roles = True)
    async def jsonsave(self, ctx):
        SAVEJSON()
        await ctx.send("SAVEJSON() called!")

    @commands.command()
    @has_permissions(manage_roles=True)
    async def evaluate(self, ctx, msg):
        eval_result = eval(msg)
        await ctx.send(eval_result)

class Answers(commands.Cog):
    @commands.command(name = "answers.getlists")
    async def answers_getlists(self, ctx):
        rlists = ""
        for x in random_answers:
            rlists += x.returnName() + '\n'
        em = discord.Embed(title = "WORD-ANSWER LIST")
        em.add_field(name = "LISTNAME", value = rlists, inline = False)
        await ctx.send(embed = em)

    @commands.command(name = "answers.getlist")
    async def answers_getlist(self, ctx, listName):
        for x in random_answers:
            if x.returnName() == listName:
                em = discord.Embed(title = listName)
                em.add_field(name = "TYPE", value = x.returnType())

                w_val = ""
                for w in x.returnWordList():
                    w_val += w + '\n'
                em.add_field(name = "WORDS", value = w_val, inline = False)

                a_val = ""
                for a in x.returnAnswerList():
                    a_val += a + '\n'
                em.add_field(name = "ANSWERS", value = a_val, inline = False)

                await ctx.send(embed = em)
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name = "answers.addlist")
    @has_permissions(manage_roles = True)
    async def answers_addlist(self, ctx, listName, listType):
        for x in random_answers:
            if x.returnName() == listName:
                await ctx.send("List already exists!")
                return

        random_answers.append(ext.word_answering_random(listName, listType.upper(), [], []))
        SAVEJSON()
        await ctx.send("List created!")

    @commands.command(name = "answers.removelist")
    @has_permissions(manage_roles = True)
    async def answers_removelist(self, ctx, listName, usure):
        if usure != "I am very sure of this!":
            await ctx.send("In the parameter 'usure', please say 'I am very sure of this!'")
            return

        for x in random_answers:
            if x.returnName() == listName:
                random_answers.remove(x)
                await ctx.send("Removed list!")
                SAVEJSON()
                return

        await ctx.send("List doesnt exist!")

    @commands.command(name = "answers.addanswertolist")
    async def answers_addanswertolist(self, ctx, listName, answer):
        for x in random_answers:
            if x.returnName() == listName:
                x.addAnswer(answer)
                SAVEJSON()
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name = "answers.addwordtolist")
    async def answers_addwordtolist(self, ctx, listName, word):
        for x in random_answers:
            if x.returnName() == listName:
                x.addWord(word)
                SAVEJSON()
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

class File(commands.Cog):
    @commands.command(name = "file.upload")
    async def file_upload(self, ctx):
        await ctx.send(f"ATTACHMENTS:{ctx.message.attachments}")
        await ctx.send("Trying to download file in host...")

        r = requests.get(ctx.message.attachments[0].url, allow_redirects = True)
        fname = "./uploads/" + ctx.message.attachments[0].filename

        await asyncio.sleep(3)
        open(fname, "wb").write(r.content)
        await asyncio.sleep(1)

        if os.path.exists(fname):
            await ctx.send("os.path.exists returned True! (file downloaded successfully)")
        else:
            await ctx.send("os.path.exists returned False! Wait a few more seconds and check the directory!")

    @commands.command(name = "file.download")
    async def file_download(self, ctx, fileName):
        path = "./uploads/" + fileName
        if os.path.exists(path) == False:
            await ctx.send(f"os.path.exists({path}) returned False! No file to download.")
            return

        await ctx.send(file = discord.File(path))

    @commands.command(name = "file.getdir")
    async def file_getdir(self, ctx):
        onlyfiles = [f for f in os.listdir("./uploads/") if os.path.isfile(os.path.join("./uploads/", f))]
        t = "\tFiles in ./uploads/\n"
        for x in onlyfiles:
            t += x + "\n"
        await ctx.send(f"`{t}`")

class RandomCommands(commands.Cog):
    @commands.command(name = "sendtobigma")
    async def sendtobigma(self, ctx, msg):
        u = await bot.fetch_user(301493792366657537)
        await u.send(msg)
        playsound("./uploads/alarm.mp3")
        await ctx.send(f"Ya le mande el dm a bigma y le puse un sonido en la pc.")
#endregion

#region BOT EVENTS    
async def sendToOwner(msg):
    u = await bot.fetch_user(301493792366657537)
    await u.send(msg)
bot = commands.Bot(command_prefix = "$")
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
LOADJSON()

bot.add_cog(Rand())
bot.add_cog(AdminOnly())
bot.add_cog(Answers())
bot.add_cog(File())
bot.add_cog(RandomCommands())

bot.run(token)
#endregion
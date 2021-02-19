from discord import file
import resources.dsbot_extensions as ext
import discord
import requests
import asyncio
import aiohttp
import random
from discord.ext import commands
from discord.ext.commands import bot
from wand.image import Image
from wand.display import display
import aiofiles


class imgflipData():
    isEnabled = False
    username = ""
    password = ""

    def __init__(self, isEnabled, username, password):
        self.isEnabled = isEnabled
        self.username = username
        self.password = password


class Memes(commands.Cog):

    imgflip = None

    def __init__(self, imgflipdata):
        super().__init__()
        self.imgflip = imgflipdata

    @commands.command(name="memes.getlist")
    async def memes_getlist(self, ctx):
        if self.imgflip.isEnabled == False:
            await ctx.send("The bot has imgflip disabled!")
            return

        url = "https://api.imgflip.com/get_memes"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                load = await resp.json()
        if load["success"] != True:
            await ctx.send("getlist['success'] returned False! cannot continue.")
            return

        with open("./temp/memelist.txt", 'w') as f:
            memelist_text = "**MEME LIST**\n"
            f.write(memelist_text)

            for meme in load["data"]["memes"]:
                id = meme["id"]
                name = meme["name"]
                f.write(f"{id}: \t\t{name}\n")

        await ctx.send(file=discord.File("./temp/memelist.txt"))

    @commands.command(name="memes.creatememe")
    async def memes_creatememe(self, ctx, template_id, text0, text1=""):
        if self.imgflip.isEnabled == False:
            await ctx.send("The bot has imgflip disabled!")
            return

        url = "https://api.imgflip.com/caption_image"
        postdata = {
            "template_id": template_id,
            "username": "Matas1",
            "password": "askdjlasdfjklhn123",
            "text0": text0,
            "text1": text1
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=postdata) as resp:
                load = await resp.json()

        if load["success"] != True:
            errormsg = load["error_message"]
            await ctx.send(f"ERROR! -> {errormsg}")
            return

        randid = random.randrange(0, 100000)
        fname = f"./temp/{randid}.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(load["data"]["url"]) as resp:
                if resp.status != 200:
                    await ctx.send("url status != 200")
                    return

                f = await aiofiles.open(fname, mode='wb')
                await f.write(await resp.read())
                await f.close()

        await ctx.send(file=discord.File(fname))

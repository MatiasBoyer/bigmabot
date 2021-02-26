import discord
import asyncio
import os
import math
import aiohttp
import aiofiles
import resources.guildsave as guildsave
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from resources.ytdownloader import YTDL_Audio, YTDL_Video


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class File(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="file.upload")
    async def file_upload(self, ctx):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/"
        if os.path.exists(path) == False:
            os.mkdir(path)

        onlyfiles = [f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))]

        maxstoragebytes = guildconf["MaxStorageBytes"]
        totalstoragebytes = 0
        for x in onlyfiles:
            size = os.path.getsize(path + x)
            totalstoragebytes += size

        if totalstoragebytes >= maxstoragebytes:
            exceded = (totalstoragebytes - maxstoragebytes)/1e+6
            await ctx.send(f"Failed to upload! The upload would result in a storage exceed of {exceded} MBs")
            return

        # await ctx.send(f"ATTACHMENTS:{ctx.message.attachments}")
        await ctx.send("Trying to download file in host...")

        #r = requests.get(ctx.message.attachments[0].url, allow_redirects=True)
        #fname = f"./guilds/{ctx.message.guild.id}/uploads/{ctx.message.attachments[0].filename}"

        # await asyncio.sleep(3)
        #open(fname, "wb").write(r.content)
        # await asyncio.sleep(1)

        url = ctx.message.attachments[0].url

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("url status != 200")
                    return

                fname = f"{path}{ctx.message.attachments[0].filename}"

                f = await aiofiles.open(fname, mode='wb')
                await f.write(await resp.read())
                await f.close()

        if os.path.exists(fname):
            await ctx.send("File downloaded successfully!")
        else:
            await ctx.send("Something went wrong downloading your file!")

    @commands.command(name="file.download")
    async def file_download(self, ctx, fileName):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/{fileName}"
        if os.path.exists(path) == False:
            await ctx.send(f"os.path.exists({path}) returned False! No file to download.")
            return

        await ctx.send(file=discord.File(path))

    @commands.command(name="file.getdir")
    async def file_getdir(self, ctx):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/"
        onlyfiles = [f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))]
        maxfilebytes = guildconf["MaxStorageBytes"]

        totalstoragebytes = 0
        t = f"\tFiles in {path}\n"

        em = discord.Embed(
            title=f"Files in {path}",
            description=f"Total storage used: {truncate(totalstoragebytes/1e+6,2)} MBs/{truncate(maxfilebytes/1e+6,2)} MBs")

        fdict = {}
        for x in onlyfiles:
            size = os.path.getsize(path + x)
            totalstoragebytes += size

            sizeinmb = truncate(size/1e+6, 2)
            fdict[x] = str(sizeinmb) + " MBs"

        L = ""
        R = ""
        for x in fdict:
            L += f"{x}\n"
            R += f"{fdict[x]}\n"

        em.add_field(name="File name", value=L, inline=True)
        em.add_field(name="Disk usage", value=R, inline=True)

        await ctx.send(embed=em)

    @ commands.command(name="file.remove")
    @ has_permissions(manage_roles=True)
    async def file_remove(self, ctx, filename):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/"
        os.remove(path + filename)

        if os.path.exists(path + filename) == False:
            await ctx.send("Removed successfuly!")
        else:
            await ctx.send("Failed to remove file!")

    @commands.command(name="dl.audiofromyt")
    async def dl_audiofromyt(self, ctx, *, url):
        msg = await ctx.send("OK! Downloading...")
        fname = ""

        async with ctx.typing():
            fname = await YTDL_Audio.download_audio(url, loop=self.bot.loop)

            await msg.delete()
            if os.path.getsize(fname) < 8e+6:
                await ctx.send(file=discord.File(fname))
            else:
                await ctx.send("File ended up being too large to send (file > 8 MB)")

        os.remove(fname)

    @commands.command(name="dl.videofromyt")
    async def dl_videofromyt(self, ctx, *, url):
        msg = await ctx.send("OK! Downloading...")
        fname = ""

        async with ctx.typing():
            fname = await YTDL_Video.download_video(url, loop=self.bot.loop)

            await msg.delete()
            if os.path.getsize(fname) < 8e+6:
                await ctx.send(file=discord.File(fname))
            else:
                await ctx.send("File ended up being too large to send (file > 8 MB)")

        os.remove(fname)

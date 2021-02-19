import discord
import asyncio
import requests
import os
import dsbot_extensions as ext
from discord.ext import commands
from discord.ext.commands.core import has_permissions


class File(commands.Cog):
    @commands.command(name="file.upload")
    async def file_upload(self, ctx):
        await ctx.send(f"ATTACHMENTS:{ctx.message.attachments}")
        await ctx.send("Trying to download file in host...")

        r = requests.get(ctx.message.attachments[0].url, allow_redirects=True)
        fname = "./uploads/" + ctx.message.attachments[0].filename

        await asyncio.sleep(3)
        open(fname, "wb").write(r.content)
        await asyncio.sleep(1)

        if os.path.exists(fname):
            await ctx.send("os.path.exists returned True! (file downloaded successfully)")
        else:
            await ctx.send("os.path.exists returned False! Wait a few more seconds and check the directory!")

    @commands.command(name="file.download")
    async def file_download(self, ctx, fileName):
        path = "./uploads/" + fileName
        if os.path.exists(path) == False:
            await ctx.send(f"os.path.exists({path}) returned False! No file to download.")
            return

        await ctx.send(file=discord.File(path))

    @commands.command(name="file.getdir")
    async def file_getdir(self, ctx):
        onlyfiles = [f for f in os.listdir(
            "./uploads/") if os.path.isfile(os.path.join("./uploads/", f))]
        t = "\tFiles in ./uploads/\n"
        for x in onlyfiles:
            t += f"{x}\t\t\t{(os.path.getsize('./uploads/' + x)/1e+6)} MBs\n"
            #t += x + "\n"
        await ctx.send(f"`{t}`")

    @commands.command(name="file.remove")
    @has_permissions(manage_roles=True)
    async def file_remove(self, ctx, filename):
        os.remove("./uploads/" + filename)
        await ctx.send("os.remove() called!")

import discord
import asyncio
import requests
import os
import math
import resources.guildsave as guildsave
import resources.dsbot_extensions as ext
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from pathlib import Path


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class File(commands.Cog):
    @commands.command(name="file.upload")
    async def file_upload(self, ctx):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/"
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

        r = requests.get(ctx.message.attachments[0].url, allow_redirects=True)
        fname = f"./guilds/{ctx.message.guild.id}/uploads/{ctx.message.attachments[0].filename}"

        await asyncio.sleep(3)
        open(fname, "wb").write(r.content)
        await asyncio.sleep(1)

        if os.path.exists(fname):
            await ctx.send("os.path.exists returned True! (file downloaded successfully)")
        else:
            await ctx.send("os.path.exists returned False! Wait a few more seconds and check the directory!")

    @commands.command(name="file.download")
    async def file_download(self, ctx, fileName):
        guildconf = guildsave.returnGuildJson(
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
        guildconf = guildsave.returnGuildJson(
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
        for x in onlyfiles:
            size = os.path.getsize(path + x)
            totalstoragebytes += size
            t += f"{x}\t\t\t\t\t{truncate(size/1e+6,1)} MBs\n"
            # t += x + "\n"
        t += f"TOTAL STORAGE USED:\t{truncate(totalstoragebytes/1e+6,1)} MBs/{truncate(maxfilebytes/1e+6,1)} MBs\n"
        await ctx.send(f"`{t}`")

    @ commands.command(name="file.remove")
    @ has_permissions(manage_roles=True)
    async def file_remove(self, ctx, filename):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        if guildconf["HasPermissionToFileCommands"] == False:
            await ctx.send("This guild has no permission to file commands!")
            return

        path = f"./guilds/{ctx.message.guild.id}/uploads/"
        os.remove(path + filename)
        await ctx.send("removefile called!")

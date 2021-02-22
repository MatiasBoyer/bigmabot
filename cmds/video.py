from cmds.rand import Rand
import resources.dsbot_extensions as ext
import discord
import asyncio
import aiohttp
import PIL
import numpy
import random
import os
from PIL import Image
from PIL import ImageOps
from discord.ext import commands
from discord.ext.commands import bot
from wand.image import Image
from wand.display import display
from io import BytesIO
from moviepy.editor import *
import aiofiles

IMAGEMAGICK_BINARY = os.getenv(
    'IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.0.11-Q16\convert.exe')


def int_tryparse(str):
    try:
        return int(str), True
    except ValueError:
        return None, False


async def process_parameter(ctx, key, val, clip):
    correct = False
    ret = clip

    rdict = {}

    if key == "set_fps":
        f = int_tryparse(val)

        if f[1] == False:
            await ctx.send(f"Error parsing '{key}={val}' into an int.")
            correct = False

        ret = clip.set_fps(f[0])
        correct = True

    if key == "top_text":
        txt = (TextClip(val, fontsize=32,
                        color='white').set_position("top").set_duration(clip.duration))
        ret = CompositeVideoClip([clip, txt])
        correct = True

    if key == "bottom_text":
        txt = (TextClip(val, fontsize=32,
                        color='white').set_position("bottom").set_duration(clip.duration))
        ret = CompositeVideoClip([clip, txt])
        correct = True

    if key == "rotate":
        f = int_tryparse(val)

        if f[1] == False:
            await ctx.send(f"Error parsing '{key}={val}' into an int.")
            correct = False

        ret = clip.rotate(f[0])
        correct = True

    if key == "bitrate":
        if 'k' not in val:
            val += 'k'

        brate = int(val[:len(val) - 1])

        if brate > 3000:
            brate = 3000

            await ctx.send("bitrate > 3000, clamping to 3000...")

        rdict["bitrate"] = val
        correct = True

    return correct, ret, rdict


class Video(commands.Cog):

    async def trygetVideo(self, ctx, *args):
        video_url = ""
        if len(ctx.message.attachments) > 0:
            video_url = ctx.message.attachments[0].url
        elif len(args) > 0:
            video_url = args[0]

        if "http" not in video_url:
            video_url = ""

        if video_url == "":
            fetched_m = await ctx.channel.history().find(lambda m: len(m.attachments) == 1)

            if fetched_m == None:
                await ctx.send("No videos found in your message.")
                return None
            else:
                video_url = fetched_m.attachments[0].url

        if video_url[len(video_url) - 4:] != ".mp4":
            await ctx.send("Video should be .mp4!")
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as resp:
                if resp.status != 200:
                    await ctx.send("url status != 200")
                    return

                fname = f"./temp/{ctx.message.id}.mp4"

                f = await aiofiles.open(fname, mode='wb')
                await f.write(await resp.read())
                await f.close()

                return fname

    @commands.command(name="vid.process")
    async def vid_process(self, ctx, *args):
        video_name = await self.trygetVideo(ctx, args)
        if video_name == None:
            return

        try:
            _args = ((' '.join(args)).split(','))
            args_dict = dict()
            for x in _args:
                splt = x.split('=')
                args_dict[splt[0].strip()] = splt[1]

            # , target_resolution=(1024, 768))
            clip = VideoFileClip(video_name)
            endclip = clip

            bitrate = "300k"

            print(args_dict)
            for i in args_dict:
                key = i
                val = args_dict[key]

                print(f"{key} : {val}")

                # , composite_list)
                pp = await process_parameter(ctx, key, val, endclip)

                if pp[0] == True:
                    endclip = pp[1]

                    for x in pp[2]:
                        if x == "bitrate":
                            bitrate = pp[2]["bitrate"]

            fname = f"{video_name}-OUT.mp4"

            print(bitrate)
            endclip.write_videofile(fname, bitrate=bitrate)

            await ctx.send(file=discord.File(fname))

            os.remove(fname)
            os.remove(video_name)
        except ValueError as v:
            await ctx.send(f"Error -> {v}")

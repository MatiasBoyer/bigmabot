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


def float_tryparse(str):
    try:
        return float(str), True
    except ValueError:
        return None, False


def write_videofile(clip, videoname, bitrate):
    return clip.write_videofile(videoname, bitrate=bitrate, audio_bitrate=bitrate)


def process_parameter(key, val, clip):
    if key == "set_fps":
        result, correct = int_tryparse(val)
        if correct == False:
            return f"Couldn't parse {key}:{val} into an integer!", False

        clip = clip.set_fps(fps=result)

        return clip, True

    if key == "top_text":
        txt = TextClip(val, fontsize=30, color='white').set_position(
            'top').set_duration(clip.duration)
        clip = CompositeVideoClip([clip, txt])

        return clip, True

    if key == "bottom_text":
        txt = TextClip(val, fontsize=30, color='white').set_position(
            'bottom').set_duration(clip.duration)
        clip = CompositeVideoClip([clip, txt])
        return clip, True

    if key == "painting":
        clip = clip.fx(vfx.painting)
        return clip, True

    if key == "mirror_x":
        clip = clip.fx(vfx.mirror_x)
        return clip, True

    if key == "mirror_y":
        clip = clip.fx(vfx.mirror_y)
        return clip, True

    if key == "blacknwhite":
        clip = clip.fx(vfx.blackwhite)
        return clip, True

    if key == "fadein":
        result, correct = float_tryparse(val)
        if correct == False:
            return f"Couldn't parse {key}:{val} into an integer!", False

        clip = clip.fx(vfx.fadein, result)
        return clip, True

    if key == "fadeout":
        result, correct = float_tryparse(val)
        if correct == False:
            return f"Couldn't parse {key}:{val} into an integer!", False

        clip = clip.fx(vfx.fadeout, result)
        return clip, True

    if key == "invert_colors":
        clip = clip.fx(vfx.invert_colors)
        return clip, True

    if key == "freeze":
        r = val.split(':')
        clip = clip.fx(vfx.freeze, t=float_tryparse(
            r[0]), freeze_duration=float_tryparse(r[1]))

        return clip, True

    return None, False


class Video(commands.Cog):
    bot = None

    def __init__(self, bot):
        self.bot = bot

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
                return None, False
            else:
                video_url = fetched_m.attachments[0].url

        if video_url[len(video_url) - 4:] != ".mp4":
            await ctx.send("Video should be .mp4!")
            return None, False

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as resp:
                if resp.status != 200:
                    await ctx.send("url status != 200")
                    return

                fname = f"./temp/{ctx.message.id}.mp4"

                f = await aiofiles.open(fname, mode='wb')
                await f.write(await resp.read())
                await f.close()

                return fname, True

    @commands.command(name="vid.process")
    async def vid_process(self, ctx, *args):
        videoname = None
        clip = None
        try:
            # GET THE VIDEO
            videoname, videoresult = await self.trygetVideo(ctx, args)
            if videoresult == False:
                return

            bitrate = '500k'
            clip = VideoFileClip(videoname)

            # PROCESS ARGUMENTS INTO A DICTIONARY FOR EASY ACCESS
            _args = ((' '.join(args)).split(','))
            arguments = dict()
            for x in _args:
                y = x.split('=')
                y.append("")

                arguments[(y[0].strip())] = y[1]

            # PROCESS EACH ARGUMENT
            for x in arguments:
                key = x
                val = arguments[x]

                if key == "bitrate":
                    if 'k' not in val:
                        val += 'k'

                    bitrate = val
                    continue

                result, correct = await self.bot.loop.run_in_executor(None, process_parameter, key, val, clip)

                if correct:
                    clip = result
                else:
                    await ctx.send(f"Error! ->{result}")

            # ONCE THE VIDEO IS COMPLETE, WE WRITE IT TO A FILE
            finalvideoname = f"./temp/{ctx.message.id}-result.mp4"
            await self.bot.loop.run_in_executor(None, write_videofile, clip, finalvideoname, bitrate)

            # WE SEND THE VIDEO!
            await ctx.send(file=discord.File(finalvideoname))

            # WE REMOVE THE TEMPORARY FILES. SPACE IS IMPORTANT!
            clip.close()

            os.remove(videoname)
            os.remove(finalvideoname)

        except Exception as e:
            await ctx.send(str(e))

            if clip != None:
                clip.close()

            if videoname != None:
                os.remove(videoname)

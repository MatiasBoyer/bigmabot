import asyncio
import discord
import time
import os
from gtts import gTTS
from discord.ext import commands
from resources.ytdownloader import YTDL_Audio
import resources.guildsave as guildsave


class Audio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def do_tts(self, ttslang, ttsmsg, filename):
        try:
            tts = gTTS(ttsmsg, lang=ttslang)
            tts.save(filename)

            return filename, True
        except Exception as e:
            return str(e), False

    @commands.command(name="tts")
    async def tts(self, ctx, *args):
        try:
            _args = ' '.join(args)

            conf = await guildsave.returnGuildJson(ctx, ctx.guild.id)
            l = conf["userConfig"]["tts_deflang"]

            if _args[:5] == "lang=":
                l = _args[5:7]
                _args = _args[7:]

            fname = f"./temp/{ctx.message.id}-tts.mp3"

            filename, correct = await self.bot.loop.run_in_executor(None, self.do_tts, l, _args, fname)

            if correct:
                await ctx.send(file=discord.File(fname))

                if ctx.message.author.voice != None:
                    voice_channel = ctx.message.author.voice.channel
                    vc = await voice_channel.connect()

                    vc.play(discord.FFmpegPCMAudio(fname))

                    # while(vc.is_playing()):
                    #    asyncio.sleep(1)

                    # await vc.disconnect()

                asyncio.sleep(5)
                os.remove(fname)
            else:
                await ctx.send(f"Error! -> {str(filename)}")

        except Exception as e:
            await ctx.send(str(e))

    @commands.command(name="vc.play")
    async def vc_youtubeplay(self, ctx, *, url):
        msg = await ctx.send("OK! Loading...")

        async with ctx.typing():
            player = await YTDL_Audio.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        duration = time.strftime(
            '%H:%M:%S', time.gmtime(float(player.duration)))
        await msg.edit(content=('Now playing: {song_name} / {song_duration}'.format(song_name=player.title, song_duration=duration)))

    @ commands.command(name="vc.leave")
    async def vc_disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @ commands.command(name="vc.volume")
    async def vc_volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = (
            volume / 100) if (volume > 0 and volume < 1) else 0.5
        await ctx.send("Changed volume to {}%".format(volume))

    @ vc_youtubeplay.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

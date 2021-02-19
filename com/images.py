import dsbot_extensions as ext
import discord
import requests
import asyncio
import aiohttp
from discord.ext import commands
from discord.ext.commands import bot
from wand.image import Image
from wand.display import display
import aiofiles


class Images(commands.Cog):

    lastImgName = ""

    async def trygetImage(self, ctx, *args):
        image_url = ""
        if len(ctx.message.attachments) > 0:
            image_url = ctx.message.attachments[0].url
        elif len(args) > 0:
            image_url = args[0]

        if image_url == "":
            await ctx.send("No images found in your message.")
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    await ctx.send("url status != 200")
                    return

                fname = f"./temp/{ctx.message.id}.png"

                f = await aiofiles.open(fname, mode='wb')
                await f.write(await resp.read())
                await f.close()

                return fname

    @commands.command(name="img.magik")
    async def image_magik(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        with Image(filename=img_name) as img:
            img.liquid_rescale(width=int(img.width * 0.5),
                               height=int(img.height * 0.5),
                               #delta_x=int(0.5 * scale) if scale else 1,
                               rigidity=0)
            img.liquid_rescale(width=int(img.width * 1.5),
                               height=int(img.height * 1.5),
                               #delta_x=scale if scale else 2,
                               rigidity=0)
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.resize")
    async def image_resize(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        i = 0
        if "://" in args[0]:
            i += 1

        percentage = float(args[i])

        if percentage >= 10:
            await ctx.send("size >= 10! Cannot proceed")
            return

        with Image(filename=img_name) as img:
            x = int(img.width * percentage)
            y = int(img.height * percentage)

            if x >= 1500 or y >= 1500:
                await ctx.send("x/y >= 1500! Cannot proceed")
                return

            img.resize(int(img.width * percentage),
                       int(img.height * percentage))

            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.rotate")
    async def image_rotate(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        i = 0
        if "://" in args[0]:
            i += 1

        deg = float(args[i])

        with Image(filename=img_name) as img:
            img.rotate(deg)
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.flip")
    async def image_flip(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        with Image(filename=img_name) as img:
            img.flip()
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.flop")
    async def image_flop(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        with Image(filename=img_name) as img:
            img.flop()
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.transparentize")
    async def image_transparentize(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        i = 0
        if "://" in args[0]:
            i += 1

        perc = float(args[i])

        if perc > 1:
            perc = 1
        if perc < 0:
            perc = 0

        with Image(filename=img_name) as img:
            img.transparentize(perc)
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.transpose")
    async def image_transpose(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        with Image(filename=img_name) as img:
            img.transpose()
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.transverse")
    async def image_transverse(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            img_name = self.lastImgName
            return

        self.lastImgName = img_name

        if img_name == None:
            return

        with Image(filename=img_name) as img:
            img.transverse()
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

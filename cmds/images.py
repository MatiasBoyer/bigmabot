from cmds.rand import Rand
import resources.dsbot_extensions as ext
import discord
import requests
import asyncio
import aiohttp
import PIL
import numpy
import random
from PIL import Image
from PIL import ImageOps
from discord.ext import commands
from discord.ext.commands import bot
from wand.image import Image
from wand.display import display
from io import BytesIO
import aiofiles


class Images(commands.Cog):

    lastImgName = ""

    async def trygetImage(self, ctx, *args):
        image_url = ""
        if len(ctx.message.attachments) > 0:
            image_url = ctx.message.attachments[0].url
        elif len(args) > 0:
            image_url = args[0]

        if "http" not in image_url:
            image_url = ""

        if image_url == "":
            fetched_m = await ctx.channel.history().find(lambda m: len(m.attachments) == 1)

            if fetched_m == None:
                await ctx.send("No images found in your message.")
                return None
            else:
                image_url = fetched_m.attachments[0].url

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
            return

        with Image(filename=img_name) as img:
            img.liquid_rescale(width=int(img.width * 0.5),
                               height=int(img.height * 0.5),
                               # delta_x=int(0.5 * scale) if scale else 1,
                               rigidity=0)
            img.liquid_rescale(width=int(img.width * 1.5),
                               height=int(img.height * 1.5),
                               # delta_x=scale if scale else 2,
                               rigidity=0)
            img.save(filename=img_name)

        await ctx.send(file=discord.File(img_name))

    @commands.command(name="img.resize")
    async def image_resize(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)

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

    @commands.command(name="img.waaw")
    async def image_waaw(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            return

        f = BytesIO()
        f2 = BytesIO()
        with Image(filename=img_name) as img:
            h1 = img.clone()
            width = int(img.width/2) if int(img.width/2) > 0 else 1
            h1.crop(width=width, height=int(img.height), gravity="east")
            h2 = h1.clone()
            h1.rotate(degree=180)
            h1.flip()

            h1.save(file=f)
            h2.save(file=f2)

        f.seek(0)
        f2.seek(0)

        im_list = [f2, f]
        imgs = [PIL.ImageOps.mirror(PIL.Image.open(
            i).convert('RGBA')) for i in im_list]
        min_shape = sorted([(numpy.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = numpy.hstack(
            (numpy.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)

        fname = f"./temp/{str(random.randrange(0, 10000))}.png"
        imgs_comb.save(fname, "PNG")

        await ctx.send(file=discord.File(fname))

    @commands.command(name="img.haah")
    async def image_haah(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            return

        f = BytesIO()
        f2 = BytesIO()
        with Image(filename=img_name) as img:
            h1 = img.clone()
            width = int(img.width/2) if int(img.width/2) > 0 else 1
            h1.crop(width=width, height=int(img.height), gravity="east")
            h2 = h1.clone()
            h2.rotate(degree=180)
            h2.flip()

            h1.save(file=f)
            h2.save(file=f2)

        f.seek(0)
        f2.seek(0)

        im_list = [f2, f]
        imgs = [PIL.ImageOps.mirror(PIL.Image.open(
            i).convert('RGBA')) for i in im_list]
        min_shape = sorted([(numpy.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = numpy.hstack(
            (numpy.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)

        fname = f"./temp/{str(random.randrange(0, 10000))}.png"
        imgs_comb.save(fname, "PNG")

        await ctx.send(file=discord.File(fname))

    @commands.command(name="img.woow")
    async def image_woow(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            return

        f = BytesIO()
        f2 = BytesIO()
        with Image(filename=img_name) as img:
            h1 = img.clone()
            width = int(img.width) if int(img.width) > 0 else 1
            h1.crop(width=width, height=int(img.height/2), gravity="north")
            h2 = h1.clone()
            h2.rotate(degree=180)
            h2.flop()

            h1.save(file=f)
            h2.save(file=f2)

        f.seek(0)
        f2.seek(0)

        im_list = [f2, f]
        imgs = [PIL.ImageOps.mirror(PIL.Image.open(
            i).convert('RGBA')) for i in im_list]
        min_shape = sorted([(numpy.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = numpy.vstack(
            (numpy.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)

        fname = f"./temp/{str(random.randrange(0, 10000))}.png"
        imgs_comb.save(fname, "PNG")

        await ctx.send(file=discord.File(fname))

    @commands.command(name="img.hooh")
    async def image_hooh(self, ctx, *args):
        img_name = await self.trygetImage(ctx, *args)
        if img_name == None:
            return

        f = BytesIO()
        f2 = BytesIO()
        with Image(filename=img_name) as img:
            h1 = img.clone()
            width = int(img.width) if int(img.width) > 0 else 1
            h1.crop(width=width, height=int(img.height/2), gravity="south")
            h2 = h1.clone()
            h2.rotate(degree=180)
            h2.flop()

            h1.save(file=f)
            h2.save(file=f2)

        f.seek(0)
        f2.seek(0)

        im_list = [f2, f]
        imgs = [PIL.ImageOps.mirror(PIL.Image.open(
            i).convert('RGBA')) for i in im_list]
        min_shape = sorted([(numpy.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = numpy.vstack(
            (numpy.asarray(i.resize(min_shape)) for i in imgs))
        imgs_comb = PIL.Image.fromarray(imgs_comb)

        fname = f"./temp/{str(random.randrange(0, 10000))}.png"
        imgs_comb.save(fname, "PNG")

        await ctx.send(file=discord.File(fname))

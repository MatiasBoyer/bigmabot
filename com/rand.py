import random
from discord.ext import commands
from discord.ext.commands.core import command, has_permissions

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
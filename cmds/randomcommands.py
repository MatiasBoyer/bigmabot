from discord.ext import commands
from discord.ext.commands.core import command, has_permissions
from cleverbot_free.cbapi import CleverBot


class RandomCommands(commands.Cog):

    cbenabled = False
    cb = CleverBot()

    def __init__(self, _bot, cbenabled):
        self.cb = CleverBot()
        self.bot = _bot
        self.cbenabled = cbenabled
        if cbenabled == True:
            self.cb.init()

    def do_cleverbot_ask(self, msg):
        try:
            response = self.cb.getResponse(' '.join(msg))
            return response, True
        except Exception as e:
            return str(e), False

    @commands.command(name="askcleverbot")
    async def cleverbot_ask(self, ctx, *msg):
        if self.cbenabled == False:
            await ctx.send("bot has this command disabled!")
            return

        try:
            m = await ctx.send("Thinking... ⏳")

            response, correct = await self.bot.loop.run_in_executor(None, self.do_cleverbot_ask,
                                                                    ' '.join(msg))

            if correct == True:
                await m.edit(content=(f"cleverbot says: {response}"))
            else:
                await m.edit(content=(f"Error! {response}"))
        except Exception as e:
            await ctx.send(str(e))
        # cb_response = cb.single_exchange(msg)

    @ commands.command(name="gitlink")
    async def gitlink(self, ctx):
        await ctx.send("https://github.com/MatiasBoyer/bigmabot")

import discord
import dsbot_extensions as ext
from discord.ext import commands
from discord.ext.commands.core import has_permissions


class Answers(commands.Cog):
    ranswers = []

    def __init__(self, ranswers) -> None:
        self.ranswers = ranswers

    @commands.command(name="answers.getlists")
    async def answers_getlists(self, ctx):
        rlists = ""
        for x in self.ranswers:
            rlists += x.returnName() + '\n'
        em = discord.Embed(title="WORD-ANSWER LIST")
        em.add_field(name="LISTNAME", value=rlists, inline=False)
        await ctx.send(embed=em)

    @commands.command(name="answers.getlist")
    async def answers_getlist(self, ctx, listName):
        for x in self.ranswers:
            if x.returnName() == listName:
                em = discord.Embed(title=listName)
                em.add_field(name="TYPE", value=x.returnType())

                w_val = ""
                for w in range(0, len(x.returnWordList())):
                    w_val += str(w) + " ->\t" + x.returnWordList()[w] + '\n'

                if len(w_val) > 0:
                    em.add_field(name="WORDS", value=w_val, inline=False)
                else:
                    em.add_field(
                        name="WORDS", value="There's no words", inline=False)

                a_val = ""
                for a in range(0, len(x.returnAnswerList())):
                    a_val += str(a) + " ->\t" + x.returnAnswerList()[a] + '\n'

                if len(a_val) > 0:
                    em.add_field(name="ANSWERS", value=a_val, inline=False)
                else:
                    em.add_field(
                        name="WORDS", value="There's no words", inline=False)

                await ctx.send(embed=em)
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name="answers.addlist")
    @has_permissions(manage_roles=True)
    async def answers_addlist(self, ctx, listName, listType):
        for x in self.ranswers:
            if x.returnName() == listName:
                await ctx.send("List already exists!")
                return

        self.ranswers.append(ext.word_answering_random(
            listName, listType.upper(), [], []))
        ext.SAVEJSON(random_answers=self.ranswers)
        await ctx.send("List created!")

    @commands.command(name="answers.removelist")
    @has_permissions(manage_roles=True)
    async def answers_removelist(self, ctx, listName, usure):
        if usure != "I am very sure of this!":
            await ctx.send("In the parameter 'usure', please say 'I am very sure of this!'")
            return

        for x in self.ranswers:
            if x.returnName() == listName:
                self.ranswers.remove(x)
                await ctx.send("Removed list!")
                ext.SAVEJSON(random_answers=self.ranswers)
                return

        await ctx.send("List doesnt exist!")

    @commands.command(name="answers.removeat")
    async def answers_removeat(self, ctx, listName, deleteWhat, index):
        if deleteWhat == "WORDS":
            for x in self.ranswers:
                if x.returnName() == listName:
                    x.removeWord(int(index))
                    await ctx.send("x.removeWord() called!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        if deleteWhat == "ANSWERS":
            for x in self.ranswers:
                if x.returnName() == listName:
                    x.removeAnswer(int(index))
                    await ctx.send("x.removeAnswer() called!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        await ctx.send(f"I don't know what '{deleteWhat}' is!")

    @commands.command(name="answers.addanswertolist")
    async def answers_addanswertolist(self, ctx, listName, answer):
        for x in self.ranswers:
            if x.returnName() == listName:
                x.addAnswer(answer)
                ext.SAVEJSON(random_answers=self.ranswers)
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name="answers.addwordtolist")
    async def answers_addwordtolist(self, ctx, listName, word):
        for x in self.ranswers:
            if x.returnName() == listName:
                x.addWord(word)
                ext.SAVEJSON(random_answers=self.ranswers)
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

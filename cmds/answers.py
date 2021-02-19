import discord
import resources.guildsave as guildsave
import resources.dsbot_extensions as ext
from discord.ext import commands
from discord.ext.commands.core import has_permissions


class Answers(commands.Cog):

    @commands.command(name="answers.getlists")
    async def answers_getlists(self, ctx):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        rlists = ""
        for x in guildconf["AnswerList"]:
            rlists += x["NAME"] + '\n'
        em = discord.Embed(title="WORD-ANSWER LIST")
        em.add_field(name="LISTNAME", value=rlists, inline=False)
        await ctx.send(embed=em)

    @commands.command(name="answers.getlist")
    async def answers_getlist(self, ctx, listName):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        for x in guildconf["AnswerList"]:
            if x["NAME"].lower() == listName.lower():
                em = discord.Embed(title=listName)
                em.add_field(name="TYPE", value=x["TYPE"])

                w_val = ""
                for w in range(0, len(x["WORDS"])):
                    w_val += str(w) + " ->\t" + x["WORDS"][w] + '\n'

                if len(w_val) > 0:
                    em.add_field(name="WORDS", value=w_val, inline=False)
                else:
                    em.add_field(
                        name="WORDS", value="There's no words", inline=False)

                a_val = ""
                for a in range(0, len(x["ANSWERS"])):
                    a_val += str(a) + " ->\t" + x["ANSWERS"][a] + '\n'

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
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        for x in guildconf["AnswerList"]:
            if x["NAME"].lower() == listName.lower():
                await ctx.send("List already exists!")
                return

        obj = ext.word_answering_random(
            listName, listType.upper(), [], [])

        guildconf["AnswerList"].append(obj.toDict())

        guildsave.saveDataToJson(str(ctx.message.guild.id), guildconf)

        await ctx.send("List created!")

    @commands.command(name="answers.removelist")
    @has_permissions(manage_roles=True)
    async def answers_removelist(self, ctx, listName, usure):
        if usure != "I am very sure of this!":
            await ctx.send("In the parameter 'usure', please say 'I am very sure of this!'")
            return

        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))

        for i in range(0, len(guildconf["AnswerList"])):
            x = guildconf["AnswerList"][i]
            if x["NAME"].lower() == listName.lower():
                del guildconf["AnswerList"][i]

                guildsave.saveDataToJson(str(ctx.message.guild.id), guildconf)
                await ctx.send("Removed list!")
                return

        await ctx.send("List doesnt exist!")

    @commands.command(name="answers.removeat")
    async def answers_removeat(self, ctx, listName, deleteWhat, index):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))
        if deleteWhat.upper() == "WORDS":
            for x in guildconf["AnswerList"]:
                if x["NAME"].lower() == listName.lower():
                    del guildconf["AnswerList"]["WORDS"][int(index)]
                    guildsave.saveDataToJson(
                        str(ctx.message.guild.id), guildconf)
                    await ctx.send("Removed word!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        if deleteWhat.upper() == "ANSWERS":
            for x in guildconf["AnswerList"]:
                if x["NAME"].lower() == listName.lower():
                    del guildconf["AnswerList"]["ANSWERS"][int(index)]
                    guildsave.saveDataToJson(
                        str(ctx.message.guild.id), guildconf)
                    await ctx.send("x.removeAnswer() called!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        await ctx.send(f"I don't know what '{deleteWhat}' is!")

    @commands.command(name="answers.addanswertolist")
    async def answers_addanswertolist(self, ctx, listName, answer):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))
        for x in guildconf["AnswerList"]:
            if x["NAME"].lower() == listName.lower():
                val = {'a': answer}
                x["ANSWERS"].append(val['a'])
                guildsave.saveDataToJson(
                    str(ctx.message.guild.id), guildconf)
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name="answers.addwordtolist")
    async def answers_addwordtolist(self, ctx, listName, word):
        guildconf = guildsave.returnGuildJson(
            str(ctx.message.guild.id))
        for x in guildconf["AnswerList"]:
            if x["NAME"].lower() == listName.lower():
                val = {'a': word}
                x["WORDS"].append(val['a'])
                guildsave.saveDataToJson(
                    str(ctx.message.guild.id), guildconf)
                await ctx.send("Added!")
                return
        await ctx.send("The list doesn't exist!")

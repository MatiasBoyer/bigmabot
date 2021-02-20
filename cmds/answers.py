import discord
import json
import resources.guildsave as guildsave
import resources.dsbot_extensions as ext
from discord.ext import commands
from discord.ext.commands.core import has_permissions


class Answers(commands.Cog):

    typesoflist = ["TEXT", "TEXTNMEDIA", "MEDIA", "REACTION"]

    @commands.command(name="answers.getlists", description="Gets all lists")
    async def answers_getlists(self, ctx):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        rlists = ""
        for x in guildconf["AnswerList"]:
            rlists += x["NAME"] + '\n'
        em = discord.Embed(title="WORD-ANSWER LIST")
        em.add_field(name="LISTNAME", value=rlists, inline=False)
        await ctx.send(embed=em)

    @commands.command(name="answers.getlist", description="Gets all the parameters of the list given")
    async def answers_getlist(self, ctx, listName):
        guildconf = await guildsave.returnGuildJson(ctx,
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
                        name="ANSWERS", value="There's no answers", inline=False)

                await ctx.send(embed=em)
                return
        await ctx.send("The list doesn't exist!")

    @commands.command(name="answers.createlist", description="ListTypes: TEXT | MEDIA | TEXTNMEDIA | REACTION\nTEXT is plain text, \nMEDIA is attachments\nTEXTNMEDIA is text + attachments\nREACTION will react to messages")
    @has_permissions(manage_roles=True)
    async def answers_createlist(self, ctx, listName, listType):
        guildconf = await guildsave.returnGuildJson(ctx,
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

    @commands.command(name="answers.removelist", description="Removes a list permanently.")
    @has_permissions(manage_roles=True)
    async def answers_removelist(self, ctx, listName, usure):
        if usure != "I am very sure of this!":
            await ctx.send("In the parameter 'usure', please say 'I am very sure of this!'")
            return

        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))

        for i in range(0, len(guildconf["AnswerList"])):
            x = guildconf["AnswerList"][i]
            if x["NAME"].lower() == listName.lower():
                del guildconf["AnswerList"][i]

                guildsave.saveDataToJson(str(ctx.message.guild.id), guildconf)
                await ctx.send("Removed list!")
                return

        await ctx.send("List doesnt exist!")

    @commands.command(name="answers.removeat", description="Removes an element in a list. deleteWhat should be ANSWERS/WORDS, and index should be the index given in $answers.getlist")
    async def answers_removeat(self, ctx, listName, deleteWhat, index):
        guildconf = await guildsave.returnGuildJson(ctx,
                                                    str(ctx.message.guild.id))
        if deleteWhat.upper() == "WORDS":
            for x in guildconf["AnswerList"]:
                if x["NAME"].lower() == listName.lower():
                    del x["WORDS"][int(index)]
                    guildsave.saveDataToJson(
                        str(ctx.message.guild.id), guildconf)
                    await ctx.send("Removed word!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        if deleteWhat.upper() == "ANSWERS":
            for x in guildconf["AnswerList"]:
                if x["NAME"].lower() == listName.lower():
                    del x["ANSWERS"][int(index)]
                    guildsave.saveDataToJson(
                        str(ctx.message.guild.id), guildconf)
                    await ctx.send("Removed answer!")
                    return
            await ctx.send(f"List '{listName}' doesn't exist!")
            return
        await ctx.send(f"I don't know what '{deleteWhat}' is!")

    @commands.command(name="answers.addanswertolist", description="Adds an answer to the list given")
    async def answers_addanswertolist(self, ctx, listName, answer):
        guildconf = await guildsave.returnGuildJson(ctx,
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

    @commands.command(name="answers.addwordtolist", description="Adds a word to the list given")
    async def answers_addwordtolist(self, ctx, listName, word):
        guildconf = await guildsave.returnGuildJson(ctx,
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

    @commands.command(name="answers.addjson", description="indev - testing", enabled=False)
    async def answers_addjson(self, ctx, *args):
        try:
            l = ' '.join(args)
            jfile = json.loads(l)
            guildconf = await guildsave.returnGuildJson(ctx,
                                                        str(ctx.message.guild.id))

            guildconf["AnswerList"].append(jfile)

            guildsave.saveDataToJson(
                str(ctx.message.guild.id), guildconf)

            await ctx.send("Added json!")
            return
        except:
            await ctx.send("Error parsing json!")

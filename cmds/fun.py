import resources.dsbot_extensions as ext
import asyncio
import discord
import random
import json
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command, has_permissions
from cleverbot_free.cbapi import CleverBot
from datetime import datetime

with open("./resources/battle_moveset.json", 'r') as f:
    moveset_file = f.read()
    moveset_json = json.loads(moveset_file)

HANGMANPICS = ['''
  +---+
  |   |\t\t{word}
      |
      |\t\t{failure}
      |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
      |\t\t{failure}
      |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
  |   |\t\t{failure}
      |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
 /|   |\t\t{failure}
      |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
 /|\  |\t\t{failure}
      |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
 /|\  |\t\t{failure}
 /    |
      |
=========''', '''
  +---+
  |   |\t\t{word}
  O   |
 /|\  |\t\t{failure}
 / \  |
      |
=========''']


def returnRandomMove():
    random.shuffle(moveset_json["MOVESET"])
    move = random.choice(moveset_json["MOVESET"])

    isCrit = (int(move["CRIT_CHANCE"]) >= random.randrange(0, 100))
    crit_multiplier = 1
    critmin = float(move["CRIT_MULTIPLIER_MIN"])
    critmax = float(move["CRIT_MULTIPLIER_MAX"])
    if isCrit == True:
        if critmin != critmax:
            crit_multiplier = random.uniform(critmin, critmax)
        else:
            crit_multiplier = 1

    damage = 0
    min = int(move["MIN_DAMAGE"])
    max = int(move["MAX_DAMAGE"])
    failed_attack = (int(move["FAIL_RATE"]) >= random.randrange(0, 100))
    if failed_attack == False:
        if isCrit == False:
            if min != max:
                damage = random.randrange(min, max)
            else:
                damage = max
        else:
            damage = max * crit_multiplier
    else:
        damage = 0

    rText = move["TEXT"]
    if isCrit == True:
        if failed_attack == False:
            rText += move["CRIT_TEXT"]

    r_move = {
        "TEXT": rText,
        "DAMAGE": ext.truncate(damage, 0),
        "SEND_DMG_MESSAGE": move["SEND_DMG_MESSAGE"],
        "DAMAGE_MSG": move["DAMAGE_MSG"]
    }

    return r_move


class Fun(commands.Cog):

    bot = None

    def __init__(self, _bot):
        super().__init__()
        self.bot = _bot

    @commands.command(name="fun.gaymeter")
    async def fun_gaymeter(self, ctx, user=None):
        await ctx.send("Gay meter says...")
        await asyncio.sleep(1)

        randnum = random.randrange(0, 100)
        m = f"{randnum}% gay. Congrats!"

        if randnum >= 75:
            m += " https://youtu.be/DP5qPb_zDUc"

        if user == None:
            await ctx.send(f"You're {m}")
        else:
            if '<' in user:
                user = user[3:]
                user = user[:len(user) - 1]

            dpy_user = await self.bot.fetch_user(user_id=int(user))

            await ctx.send(f"{dpy_user.mention} is {m}")

    @commands.command(name="fun.battle")
    async def fun_battle(self, ctx, user_a, user_b=None):
        if user_b == None:
            user_b = user_a
            user_a = ctx.author.id

        user_a = str(user_a)
        user_b = str(user_b)

        if '<' in user_a:
            user_a = user_a[3:len(user_a) - 1]
        if '<' in user_b:
            user_b = user_b[3:len(user_b) - 1]

        user_a_m = await self.bot.fetch_user(user_id=int(user_a))
        user_b_m = await self.bot.fetch_user(user_id=int(user_b))

        await ctx.send(f"A battle between {user_a_m.mention} and {user_b_m.mention} !")
        await ctx.send(file=discord.File("./resources/media/battle.jpg"))

        user_a_hp = 100
        user_b_hp = 100

        hp_text = f"{user_a_m.mention}'s HP: {user_a_hp}%\n{user_b_m.mention}'s HP: {user_b_hp}%"
        hp_msg = await ctx.send(hp_text)

        users = [user_a_m, user_b_m]
        current_turn = random.randrange(0, 100)
        if current_turn >= 50:
            current_turn = 1
        else:
            current_turn = 0

        everybody_alive = ((user_a_hp > 0) and (user_b_hp > 0))
        while(everybody_alive):
            current_move = returnRandomMove()

            attacker = users[current_turn]
            if current_turn == 0:
                atd = 1
            else:
                atd = 0
            attacked = users[atd]

            t = current_move["TEXT"]
            dmg = current_move["DAMAGE"]

            await ctx.send(t.format(attacker=attacker, attacked=attacked))
            await asyncio.sleep(1)

            if dmg == 0:
                if current_move["SEND_DMG_MESSAGE"] == True:
                    await ctx.send("... But failed!")
            elif current_move["SEND_DMG_MESSAGE"] == True:
                if len(current_move["DAMAGE_MSG"]) < 2:
                    await ctx.send(f"... and did {dmg}% of damage!")
                else:
                    await ctx.send(current_move["DAMAGE_MSG"].format(attacker=attacker, attacked=attacked, damage=dmg))

                if user_a_m == attacker:
                    user_b_hp -= dmg
                elif user_a_m == attacked:
                    user_a_hp -= dmg

                if user_a_hp < 0:
                    user_a_hp = 0

                if user_b_hp < 0:
                    user_b_hp = 0

                # if user_b_m == attacker:
                #    user_a_hp -= dmg
                # elif user_b_m == attacked:
                #    user_b_hp -= dmg

                hp_text = f"{user_a_m.mention}'s HP: {user_a_hp}%\n{user_b_m.mention}'s HP: {user_b_hp}%"
                await hp_msg.edit(content=hp_text)

            if current_turn == 0:
                current_turn = 1
            else:
                current_turn = 0

            everybody_alive = ((user_a_hp > 0) and (user_b_hp > 0))
            await asyncio.sleep(1)

        winner = None
        if user_a_hp > 0:
            winner = user_a_m
        elif user_b_hp > 0:
            winner = user_b_m
        await ctx.send(f"Ding ding ding! We have a winner! {winner.mention} wins!")

    @commands.command("fun.hangman")
    async def hangman(self, ctx):
        await ctx.author.send("Please tell me which word you want to play in HANGMAN!\nPlease keep in mind that if your message has UNDERSCORES, it will not work.")
        await ctx.send(f"{ctx.author.mention} i've sent you a DM! Please answer it to play HANGMAN!")

        def check_author(m):
            if '_' in m.content:
                return False

            return m.author == ctx.author and isinstance(m.channel, discord.channel.DMChannel)

        def check_channel(m):
            return m.channel == ctx.channel

        def findIndex(s, ch):
            return [i for i, ltr in enumerate(s) if ltr == ch]

        msg = await self.bot.wait_for('message', check=check_author)

        hangman_inprocess = True

        hangman_word = list(msg.content.upper())
        hangman_message = ['_']*len(hangman_word)

        for x in range(0, len(hangman_word)):
            if hangman_word[x] == ' ':
                hangman_message[x] = ' '

        def setletter(letter):
            for x in range(0, len(hangman_word)):
                if hangman_word[x] == letter:
                    hangman_message[x] = letter

        failures = []
        max_failures = len(HANGMANPICS)

        def returnMessage():
            return f"`{HANGMANPICS[len(failures)]}`".format(word=(''.join(hangman_message)), failure=''.join(failures))

        sent_message = await ctx.send(returnMessage())
        while(hangman_inprocess and len(failures) < max_failures):
            msg = await self.bot.wait_for('message', check=check_channel)

            msg_content = msg.content.upper()

            if msg_content == "END_HANGMAN":
                await ctx.send("HANGMAN game ended!")
                hangman_inprocess = False
                return

            if msg_content == ''.join(hangman_word):
                await ctx.send(f"Ding ding ding! {msg.author.mention} won everything! The word was {''.join(hangman_word)}")
                return

            if len(msg_content) != 1:
                continue

            letter = msg_content[0]
            if letter in hangman_word:
                # await ctx.send(f"Letter {letter} is correct!")
                setletter(letter)

                await sent_message.edit(content=(returnMessage()))
            else:
                failures.append(letter)
                await ctx.send(f"Letter {letter} is INcorrect!")
                await sent_message.edit(content=(returnMessage()))

            if '_' not in hangman_message:
                await ctx.send(f"Congrats! The word was {''.join(hangman_word)}")

                hangman_inprocess = False
                return

        if len(failures) >= max_failures:
            await ctx.send(f"You lost! The word was {''.join(hangman_word)}")
            return

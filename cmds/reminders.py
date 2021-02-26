import csv
import uuid
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import discord
import asyncio
from discord.ext import commands
from discord.ext import tasks


def convertTo_datetime(text: str):
    try:
        t = datetime.strptime(text, '%m/%d/%Y %H:%M')
        return True, t
    except Exception as e:
        print(F"ERROR -> {e}")
        return False, None


def convertTo_datetext(time: datetime):
    try:
        t = time.strftime("%m/%d/%Y %H:%M")
        return True, t
    except Exception as e:
        print(F"ERROR -> {e}")
        return False, None


def return_currentDateTime():
    return datetime.now().strftime("%m/%d/%Y %H:%M")


repeat_types = "NONE DAILY WEEKLY MONTHLY YEARLY"


async def send_tochannelid(channelid: int, text: str, bot: commands.Bot) -> bool:
    try:
        channel = await bot.fetch_channel(channelid)
        await channel.send(f"Reminder!\n{text}")

        return True, ""
    except Exception as e:
        return False, str(e)


class CSV_WR():

    def __init__(self, filename, delimiter):
        self.filename = filename
        self.file = open(filename, newline='',
                         encoding="utf-8", errors='replace')
        self.data = list(csv.reader(self.file, delimiter=delimiter))

        # CLEANUP
        cleanup_matches = [x for x in self.data if convertTo_datetime(
            x[1])[1] < datetime.now()]

        for x in cleanup_matches:
            print("Old reminder found, removing...")
            self.data.remove(x)

        self.save_data()

    def save_data(self):
        with open(self.filename, 'w', encoding="utf-8", errors='replace') as file:
            for x in self.data:
                file.write(f"{';'.join(x)}\n")

    def return_data_rc(self, row: int, column: int):
        return self.data[row][column]

    def return_withchannelid(self, channelid: int):
        matches = [x for x in self.data if x[0] == str(channelid)]
        return matches

    def return_dateContains(self, t: str):
        matches = [x for x in self.data if t in x[1]]
        return matches

    def create_reminder(self, channel_id: int, _datetime: str, text: str, repeatType: str, add_automatically=False):
        if repeatType not in repeat_types:
            return False, "REPEAT TYPE NOT ACCEPTED"

        correct, dt_result = convertTo_datetime(_datetime)
        if correct == False:
            return False, "DATETIME PARSE FAILED"
        else:
            if dt_result.date() < datetime.now().date():
                return False, "DATETIME ALREADY PASSED"

        ret = (
            f"{str(channel_id)};{_datetime};00/00/0000 00:00;{text};{repeatType};{str(uuid.uuid4())}")
        if add_automatically:
            self.data.append(ret.split(';'))
            self.save_data()

        return True, ret

    async def do_date(self, dateObj, bot: commands.Bot):
        #dateObj[2] = dateObj[1]
        correct, date_time = convertTo_datetime(dateObj[1])

        if correct == False:
            print("An error happened whilst parsing date_time !")
            return False

        self.data.remove(dateObj)

        dateObj[2] = dateObj[1]
        dateObj[4] = dateObj[4].upper()

        if dateObj[4] == "NONE":
            # self.data.remove(dateObj)
            self.save_data()

            return await send_tochannelid(int(dateObj[0]), dateObj[3], bot)

        if dateObj[4] == "DAILY":
            # self.data.remove(dateObj)

            dateObj[1] = convertTo_datetext(
                date_time + relativedelta(days=1))[1]

            self.data.append(
                [dateObj[0], dateObj[1], dateObj[2], dateObj[3], dateObj[4], dateObj[5]])

            self.save_data()

            return await send_tochannelid(int(dateObj[0]), dateObj[3], bot)

        if dateObj[4] == "WEEKLY":
            # self.data.remove(dateObj)

            dateObj[1] = convertTo_datetext(
                date_time + relativedelta(weeks=+1))[1]

            self.data.append(
                [dateObj[0], dateObj[1], dateObj[2], dateObj[3], dateObj[4], dateObj[5]])

            self.save_data()

            return await send_tochannelid(int(dateObj[0]), dateObj[3], bot)

        if dateObj[4] == "MONTHLY":
            # self.data.remove(dateObj)

            dateObj[1] = convertTo_datetext(
                date_time + relativedelta(months=+1))[1]

            self.data.append(
                [dateObj[0], dateObj[1], dateObj[2], dateObj[3], dateObj[4], dateObj[5]])

            self.save_data()

            return await send_tochannelid(int(dateObj[0]), dateObj[3], bot)

        if dateObj[4] == "YEARLY":
            # self.data.remove(dateObj)

            dateObj[1] = convertTo_datetext(
                date_time + relativedelta(years=+1))[1]

            self.data.append(
                [dateObj[0], dateObj[1], dateObj[2], dateObj[3], dateObj[4], dateObj[5]])

            self.save_data()

            return await send_tochannelid(int(dateObj[0]), dateObj[3], bot)

        print("?")
        return False, "ERROR!"


REMINDER_CSV = CSV_WR("./guilds/reminderslist.csv", ';')


@tasks.loop(seconds=0.5)
async def getcurrent_n_sendtoall(bot: commands.Bot):
    right_now = REMINDER_CSV.return_dateContains(return_currentDateTime())

    if len(right_now) == 0:
        return

    # print(right_now)
    for x in right_now:
        await REMINDER_CSV.do_date(x, bot)


class Reminders(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        getcurrent_n_sendtoall.start(bot)

    @commands.command(name="reminder.create",
                      help="WHEN is the date, it should be in the format of 'MM/DD/YYYY HH:MM'\n" +
                      "WHAT is the text to send\n" +
                      "WHERE is the channel where to send the text to (#channel_name) (defaults to the channel where you send the command)\n" +
                      "REPEAT can be NONE/DAILY/WEEKLY/MONTHLY/YEARLY (defaults to NONE)\n" +
                      "ex: $reminder.create '02/25/2021 00:00' 'Hello everyone!' #CHANNEL 'MONTHLY'")
    async def reminder_create(self, ctx, when: str, what: str, where: discord.TextChannel = None, repeat: str = "NONE"):
        if where == None:
            where = ctx.channel

        correct, t = convertTo_datetime(when)
        if correct == False:
            await ctx.send(t)
            return

        correct, ret = REMINDER_CSV.create_reminder(
            where.id, when, what, repeat, True)
        if correct == False:
            await ctx.send(ret)
            return

        await ctx.send("Successfuly created!")
        return

import json
import time
import os
import sqlite3
from pathlib import Path

# SQL DBs


# JSON DBs
defaultsjson = None
defaultsdata = None
with open("./guilds/guilddefaults.json", 'r') as f:
    defaultsdata = f.read()
defaultsjson = json.loads(defaultsdata)


def createNewGuildJson(guildId):
    Path(f"./guilds/{guildId}").mkdir(parents=True, exist_ok=True)
    Path(f"./guilds/{guildId}/uploads").mkdir(parents=True, exist_ok=True)

    path = f"./guilds/{guildId}/guild.json"
    defaultspath = "./guilds/guilddefaults.json"

    defaultdata = None
    with open(defaultspath, 'r') as defaultsfile:
        defaultdata = defaultsfile.read()

    with open(path, 'w') as file:
        file.write(defaultdata)

    with open(path, 'r') as file:
        fjsondata = json.loads(file.read())

    return fjsondata


def saveDataToJson(guildId, data):
    path = f"./guilds/{guildId}/guild.json"
    try:
        jdump = json.dumps(data, ensure_ascii=False)
        with open(path, 'w', encoding="utf-16") as f:
            f.write(jdump)
    except Exception:
        print("Error saving!!!")


async def returnGuildJson(ctx, guildId):
    path = f"./guilds/{guildId}/guild.json"

    if os.path.exists(path):
        filedata = None
        filejson = None
        with open(path, 'r', encoding="utf-16") as file:
            filedata = file.read()

        try:
            filejson = json.loads(filedata)
        except ValueError as a:
            msg = f"Exception whilst returning the json!: {a}"
            await ctx.send(msg)
            return

        for x in defaultsjson:
            filejson.setdefault(x, defaultsjson[x])

        saveDataToJson(guildId, filejson)
        return filejson

    return createNewGuildJson(guildId)


def setKeyInGuildJson(guildId, key, value):
    gjson = returnGuildJson(guildId)

    gjson[key] = value

    saveDataToJson(guildId, gjson)

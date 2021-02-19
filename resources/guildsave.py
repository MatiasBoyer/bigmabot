import json
import time
import os
from pathlib import Path

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
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def returnGuildJson(guildId):
    path = f"./guilds/{guildId}/guild.json"

    if os.path.exists(path):
        filedata = None
        filejson = None
        with open(path, 'r') as file:
            filedata = file.read()
        filejson = json.loads(filedata)

        for x in defaultsjson:
            filejson.setdefault(x, defaultsjson[x])

        saveDataToJson(guildId, filejson)
        return filejson

    return createNewGuildJson(guildId)


def setKeyInGuildJson(guildId, key, value):
    gjson = returnGuildJson(guildId)

    gjson[key] = value

    saveDataToJson(guildId, gjson)

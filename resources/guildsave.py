import json
import time
import os
from pathlib import Path


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
        with open(path, 'r') as file:
            filedata = file.read()

        # print(filedata)
        return json.loads(filedata)

    return createNewGuildJson(guildId)


def setKeyInGuildJson(guildId, key, value):
    gjson = returnGuildJson(guildId)

    gjson[key] = value

    saveDataToJson(guildId, gjson)

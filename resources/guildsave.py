import json
import time
import os


def createNewGuildJson(guildId):
    path = f"./guilds/{guildId}.json"
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
    path = f"./guilds/{guildId}.json"
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def returnGuildJson(guildId):
    path = f"./guilds/{guildId}.json"

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

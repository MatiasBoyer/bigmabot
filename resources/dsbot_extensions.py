from os import name
import random
import json
import math


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def arrayToStrWithoutQuotationMarks(arr):
    ret = "["
    for x in range(0, len(arr)):
        ret += arr[x]
        if x < len(arr) - 1:
            ret += ","
    return ret


def isAdmitedMediaType(mediatypelist, filename):
    for x in mediatypelist:
        if x in filename:
            return True
    return False


class word_answering_random():

    name = ""
    answertype = "TEXT"
    wordlist = []
    answerlist = []

    def __init__(self, _name, _answertype, _wordlist, _answerlist):
        self.name = _name
        self.answertype = _answertype
        self.wordlist = _wordlist
        self.answerlist = _answerlist

    def returnName(self):
        return self.name

    def returnWordList(self):
        return self.wordlist

    def returnType(self):
        return self.answertype

    def addWord(self, text):
        self.wordlist.append(text)

    def returnAnswerList(self):
        return self.answerlist

    def addAnswer(self, text):
        self.answerlist.append(text)

    def removeWord(self, id):
        del self.wordlist[id]

    def removeAnswer(self, id):
        del self.answerlist[id]

    def checkword(self, text):
        for w in self.wordlist:
            if w.upper() in text.upper():
                return random.choice(self.answerlist)
        return None

    def toJson(self):
        #d = "{" + f" \"NAME\": {self.name}, \"WORDS\": {self.wordlist}, \"ANSWERS\": {self.answerlist}" + "}"
        # fix

        d = """"NAME": "{0}", "TYPE": "{1}", "WORDS": {2}, "ANSWERS": {3}""".format(
            self.name, self.answertype, self.wordlist, self.answerlist)
        x = d.replace("\'", "\"")
        return "{ " + x + " }"

    def toDict(self):
        d = {
            "NAME": self.name,
            "TYPE": self.answertype,
            "WORDS": self.wordlist,
            "ANSWERS": self.answerlist
        }

        return d


# def savedatatofile(f, data):
#    with open(f, 'w', encoding="utf-8") as file:
#        file.write(data)
#
#
# def returndatafromfile(f):
#    with open(f) as json_File:
#        data = json.load(json_File)
#        return data
#
#
# def LOADJSON(random_answers):
#    random_answers.clear()
#    answerlist = returndatafromfile("./config/answerlist.json")
#    for x in answerlist["LIST"]:
#        a = word_answering_random(
#            x["NAME"], x["TYPE"], x["WORDS"], x["ANSWERS"])
#        random_answers.append(a)
#
#
# def SAVEJSON(random_answers):
#    answerstojson = []
#    j = "{ " + "\"LIST\": "
#
#    for x in random_answers:
#        answerstojson.append(x.toJson())
#    atojson = j + arrayToStrWithoutQuotationMarks(answerstojson) + "]}"
#    # print(atojson)
#    savedatatofile("./config/answerlist.json", atojson)

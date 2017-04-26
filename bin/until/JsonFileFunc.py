#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
import json
import codecs
L = Logger.getInstance()

class JsonFileFunc(object):
    def __init__(self):
        pass

    # read content
    def readFile(self, filePath):
        jsonData = None
        try:
            with open(filePath, 'r') as tmpFile:
                jsonData = json.load(tmpFile)
        except Exception as e:
            L.printError("read [ " + str(filePath) + " ] not exists")
            L.printError("errorMsg:" + str(e))
        return jsonData

    # create json File
    def createFile(self, filePath, data):
        try:
            with codecs.open(filePath, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            L.printFalat('create ' + str(filePath) + ' fail')
            L.printError("errorMsg:" + str(e))


def getInstance():
    return JsonFileFunc()

#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
from bin import until

class PR(object):
    def __init__(self):
        self.code = until.Code_OK
        self.msg = "ok"
        self.result = None

    def setCode(self, code=1):
        self.code = code

    def setMsg(self, msg="ok"):
        self.msg = msg

    def setResult(self, result):
        self.result = result

    def getCode(self):
        return self.code

    def getMsg(self):
        return self.msg

    def getResult(self):
        return self.result

    def getPRBytes(self):
        return bytes(self.getPRStr(), encoding='utf-8')

    def getPR(self):
        return self

    def getPRStr(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def getInstance():
    return PR()

#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Path
from bin.until import JsonFileFunc
from bin.until import PR

P = Path.getInstance()
J = JsonFileFunc.getInstance()
_PR = PR.getInstance()


class Service_logic(object):
    def logic(self, data):
        _PR.setResult([{"s": "ssss"}, {"h": "hhhhh"}, {"t": "ttttt"}])
        return _PR.getPRBytes()

    def xx(self, data):
        print(data)
        return "abc"

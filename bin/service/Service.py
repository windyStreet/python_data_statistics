#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.logic.Service_logic import *
from bin.until import PR
from bin import until

_PR=PR.getInstance()


operator = \
    {
        "logic": Service_logic().logic,
        "xx": Service_logic().xx
    }

class Service(tornado.web.RequestHandler):
    def get(self):
        try:
            method = self.get_argument('method', '__error__')
            if method == "__error__":
                _PR.setCode(until.Code_METHODERROR)
                _PR.setMsg("method ERROR , not give the method or get the method is __error__")
                return self.write(_PR.getPRBytes())
            data = self.get_argument('data', None)
            self.write(operator.get(method)(data))
        except Exception as e:
            _PR.setCode(until.Code_EXCEPTION)
            _PR.setMsg("exception ERROR :"+str(e))
            self.write(_PR.getPRBytes())


    def post(self):
        self.get()

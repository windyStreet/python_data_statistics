#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.logic.Service_logic import *

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
                return "error method"
            data = self.get_argument('data', None)
            self.write(operator.get(method)(data))
        except Exception as e:
            self.write("error")
            print(e)

    def post(self):
        self.get()

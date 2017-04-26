#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.logic.Service_logic import Service_logic

SL = Service_logic()

class yy(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        greeting1 = self.get_argument('greeting1', 'kk')
        # self.write(SL.logic(greeting, greeting1))
        self.render(SL.logic())

    def post(self):
        self.get()

class aa(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        greeting1 = self.get_argument('greeting1', 'kk')
        # self.write(SL.logic(greeting, greeting1))
        self.render(SL.logic())

    def post(self):
        self.get()
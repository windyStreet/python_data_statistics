#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from bin.until import Path

htmlPath = Path.getInstance().htmlPath


class index(tornado.web.RequestHandler):
    def get(self):
        self.render(htmlPath + self.request.path)


class main(tornado.web.RequestHandler):
    def get(self):
        self.render(htmlPath + self.request.path)


class interface_statistics(tornado.web.RequestHandler):
    def get(self):
        self.render(htmlPath + self.request.path)


class line_test(tornado.web.RequestHandler):
    def get(self):
        self.render(htmlPath + self.request.path)

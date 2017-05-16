#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.init import DB_init
from bin.init import MongoDB_log
from bin.until import Logger

L = Logger.getInstance()


class Init(object):
    def __init__(self):
        pass

    def init(self):
        DB_init.getInstance().start()
        L.info("start receive mongodb log")
        MongoDB_log.getInstance().start()
        pass


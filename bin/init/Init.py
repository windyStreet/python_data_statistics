#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.init import DB_init
from bin.init import MongDB_log
from bin.until import Logger

L = Logger.getInstance()


class Init(object):
    def __init__(self):
        pass

    def init(self):
        L.info("start sys ,init DB_ds")
        DB_init.getInstance().init_DB_ds()
        L.info("start receive mongodb log")
        MongDB_log.getInstance().start()

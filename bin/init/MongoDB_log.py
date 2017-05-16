#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.init import RabbitMQ_mongo_log
from bin.until import Mongo
from bin.until import Path
from bin.until import Logger
import time
import json
import threading

MQ = RabbitMQ_mongo_log.getInstance()
P = Path.getInstance()
L = Logger.getInstance("init.log")


class MongDB_log(object):
    def __init__(self):
        pass

    def insert_log(self, ch, method, properties, body):
        L.info("insert data:%s", body)
        collection = Mongo.getInstance(table="YXYBB_interface", dbname="YXYBB").collection
        collection.insert(json.loads(str(body, encoding="utf-8")))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        pass

    def recvLog(self):
        MQ.recvMsg(queue="Mongodb_log", callback=self.insert_log)

    def start(self):
        t = threading.Thread(target=self.recvLog)
        t.start()


def getInstance():
    return MongDB_log()

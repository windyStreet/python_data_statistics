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
global counter
counter = 0


class MongoDB_log(object):
    def __init__(self):
        pass

    def insert_log(self, ch, method, properties, body):
        try:
            L.info("insert data:%s", body)
            mongo_instance = Mongo.getInstance(table="YXYBB_interface", ds="YXYBB")
            collection = mongo_instance.getCollection()
            collection.insert(json.loads(str(body, encoding="utf-8")))
            mongo_instance.close()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            global counter
            #print(counter)
            counter = counter + 1
            print(method.delivery_tag)
            #ch.basic_ack(delivery_tag=method.delivery_tag,multiple=True)
        except Exception as e:
            L.warning("insert_log Exception %s", e)
        pass

    def recvLog(self):
        MQ.recvMsg(queue="Mongodb_log", callback=self.insert_log)

    def start(self):
        t = threading.Thread(target=self.recvLog)
        t.start()


def getInstance():
    return MongoDB_log()

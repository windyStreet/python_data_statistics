#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.init import RabbitMQ_mongo_log
from bin.until import Mongo
from bin.until import Path
from bin.until import Logger
from bin.until import Time
from bin import init
import time
import json
import threading

MQ = RabbitMQ_mongo_log.getInstance()
P = Path.getInstance()
L = Logger.getInstance("init.log")
global insert_interval_time_stamp
insert_interval_time_stamp = Time.getNowTimeStamp()


class MongoDB_log(object):
    def __init__(self):
        self.delivery_tags = []
        self.insert_datas = []
        self.time_interval = 0
        pass

    def insert_log(self, ch, method, properties, body):
        self.insert_datas.append(json.loads(str(body, encoding="utf-8")))
        self.delivery_tags.append(method.delivery_tag)
        is_ack = False
        global insert_interval_time_stamp
        now_time_stamp = Time.getNowTimeStamp()
        interval_time = now_time_stamp - insert_interval_time_stamp
        if len(self.insert_datas) >= init.MAX_INSERT_COUNT or interval_time > init.INSERT_INETRVAL_TIME:
            insert_interval_time_stamp = Time.getNowTimeStamp()
            is_ack = True
            try:
                L.info("will insert data count: is %f", len(self.insert_datas))
                mongo_instance = Mongo.getInstance(table="YXYBB_interface", ds="YXYBB")
                collection = mongo_instance.getCollection()
                collection.insert_many(self.insert_datas)
                mongo_instance.close()
                self.insert_datas = []
            except Exception as e:
                L.warning("insert_log Exception %s", e)
        if is_ack is True:
            for delivery_tag in self.delivery_tags:
                ch.basic_ack(delivery_tag=delivery_tag)
            self.delivery_tags = []
        pass

    def recvLog(self):
        MQ.recvMsg(queue="Mongodb_log", callback=self.insert_log)

    def start(self):
        t = threading.Thread(target=self.recvLog)
        t.start()


def getInstance():
    return MongoDB_log()

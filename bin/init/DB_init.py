#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
from bin.until import Path
from bin.until import JsonFileFunc
from bin.until import Mongo
import os

L = Logger.getInstance()
J = JsonFileFunc.getInstance()
P = Path.getInstance()


class DB_init(object):
    def __init__(self):
        self.ds_code = None  # 数据源code值（唯一）
        self.project = None  # 项目（唯一）
        pass

    def init_DB_ds(self):
        path = P.confDirPath + os.sep + "project_ds.json"
        project_ds_info = J.readFile(path)
        collection = Mongo.getInstance(table="project_ds", ds='base').collection
        collection.remove({})  # 先删除表中所有数据
        for key in project_ds_info.keys():
            value = project_ds_info[key]
            data = {}
            data["ds_code"] = key
            data["project"] = value
            L.info("init DB_ds , insert data:" + key + ":" + value)
            collection.insert(data)
        pass


def getInstance():
    return DB_init()

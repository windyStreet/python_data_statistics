#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
from bin.until import Path
from bin.until import JsonFileFunc
from bin.until import Mongo
from bin.init import Statistical_compute_init
import os

L = Logger.getInstance()
J = JsonFileFunc.getInstance()
P = Path.getInstance()


class DB_init(object):
    def __init__(self):
        self.ds_code = None  # 数据源code值（唯一）
        self.project = None  # 项目（唯一）
        pass

    # 初始化Ds 数据库
    def init_DB_ds(self):
        path = P.confDirPath + os.sep + "DB.json"
        DB_infos = J.readFile(path)
        collection = Mongo.getInstance(table="project_ds", ds='base').collection
        collection.remove({})  # 先删除表中所有数据
        datas = []
        for key in DB_infos.keys():
            value = DB_infos[key]['dbname']
            data = {}
            data["ds_code"] = key
            data["project"] = value
            datas.append(data)
            L.info("init DB_ds , insert data:" + key + ":" + value)
        collection.insert_many(datas)
        pass


    def start(self):
        # 初始化数据源
        L.info("start sys , init DB_ds ")
        self.init_DB_ds()

        # 初始化统计项信息 (该工作可以置后处理)
        #L.info("start sys , init statistical_item ")
        #Statistical_item_init.Statistical_item_init.start()

        # 启动统计计算项任务
        L.info("start sys , compute all count data ")
        Statistical_compute_init.Statistical_compute_init().start_inti()


def getInstance():
    return DB_init()


# if __name__ == "__main__":
#     DB_init().statistical_item_init()

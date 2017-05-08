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

    #初始化Ds 数据库
    def init_DB_ds(self):
        path = P.confDirPath + os.sep + "DB.json"
        DB_infos = J.readFile(path)
        collection = Mongo.getInstance(table="project_ds", ds='base').collection
        collection.remove({})  # 先删除表中所有数据
        datas=[]
        for key in DB_infos.keys():
            value = DB_infos[key]['dbname']
            data = {}
            data["ds_code"] = key
            data["project"] = value
            datas.append(data)
            L.info("init DB_ds , insert data:" + key + ":" + value)
        collection.insert_many(datas)
        pass

    #计算统计数据
    def compute_count(self,collection,statistical_type,statistical_lastTime):
        pass

    #计算所有的统计数据
    '''statistical_item={
            "id":"主键",
            "project_name":"项目名称",
            "createtime":"数据创建时间",
            "updatetime":"数据更新时间",
            "statistical_type":"统计类型",
            "statistical_lastTime":"最后一次统计时间"，
            "statistical_startTime":"起始统计时间",
            "statistical_step":"统计频率",
        }
    '''
    def compute_count_all(self):
        collection = Mongo.getInstance(table="statistical_item", ds='base').collection
        pass

    def start(self):
        L.info("start sys , init DB_ds ")
        self.init_DB_ds()
        L.info("start sys , compute all count data ")
        self.compute_count_all()


def getInstance():
    return DB_init()

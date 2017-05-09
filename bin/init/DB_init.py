#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Logger
from bin.until import Path
from bin.until import JsonFileFunc
from bin.until import Mongo
from bin.logic.BO import statistical_item_BO
import threading
import os
import time

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

    # 计算统计数据
    def compute_count(self, collection, statistical_type, statistical_lastTime):
        pass

    # 计算同一个步长的数据（每次开启一个线程进行处理）
    def compute_step_infos(self, statistical_step_datas):
        #print("BB" + str(statistical_step_datas))
        while True:
            step = 60  # 默认一个小时，方式出现死循环问题
            for statistical_step_data in statistical_step_datas:
                #step = statistical_step_data['statistical_step']
                step = 6
                #print(statistical_step_data)
                L.debug(statistical_step_data)
            L.debug(threading.current_thread().getName())
            time.sleep(step * 1)
        pass

    # 计算所有的统计数据
    '''
    statistical_item={
            "id":"主键",
            "project_name":"项目名称",
            "createtime":"数据创建时间",
            "updatetime":"数据更新时间",
            "statistical_type":"统计类型",
            "statistical_lastTime":"最后一次统计时间"，
            "statistical_startTime":"起始统计时间",
            "statistical_step":"统计频率",
            "statistical_name“:"统计名称"
        }

    '''

    def compute_count_all(self):
        collection = Mongo.getInstance(table="statistical_item", ds='base').collection
        statistical_item_infos = collection.find({}).sort("statistical_step", 1)
        for statistical_item_info in statistical_item_infos:
            pass
            # print(statistical_item_info)
        # 1 查询库中全部的定时任务项
        # 2 按照时长进行分类这你
        pass

    def statistical_item_init(self):
        '''
         "id":"主键",
            "project_name":"项目名称",
            "createtime":"数据创建时间",
            "updatetime":"数据更新时间",
            "statistical_type":"统计类型",
            "statistical_lastTime":"最后一次统计时间"，
            "statistical_startTime":"起始统计时间",
            "statistical_step":"统计频率",
            "statistical_name“:"统计名称"
        '''

        collection = Mongo.getInstance(table="statistical_item", ds='base').collection
        statistical_datas = collection.find({}).sort("statistical_step", 1)

        statistical_step_min = 0
        statistical_step_datas = []
        for statistical_data in statistical_datas.sort("statistical_step"):
            statistical_step = statistical_data['statistical_step']
            if statistical_step_min == statistical_step or statistical_step_min is 0:
                statistical_step_min = statistical_step
                statistical_step_datas.append(statistical_data)
            else:
                # 开启一个线程处理这个频率段的数据
                t = threading.Thread(target=self.compute_step_infos, args=(statistical_step_datas,))
                t.setDaemon(True)
                t.start()
                statistical_step_min = statistical_step
                del statistical_step_datas[:]
                statistical_step_datas.append(statistical_data)
        # 开启一个线程处理这个频率段的数据
        t = threading.Thread(target=self.compute_step_infos, args=(statistical_step_datas,))
        t.setDaemon(True)
        t.start()

        # YXYBB_datas =[]
        # YXYBB_interface_1 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("interface").set_statistical_step(60*1).json
        # YXYBB_interface_2 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("interface").set_statistical_step(60*6).json
        # YXYBB_interface_3 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("interface").set_statistical_step(60*12).json
        #
        # YXYBB_interface_4 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("click").set_statistical_step(60*1).json
        # YXYBB_interface_5 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("click").set_statistical_step(60*6).json
        # YXYBB_interface_6 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("click").set_statistical_step(60*12).json
        #
        # YXYBB_datas.append(YXYBB_interface_1)
        # YXYBB_datas.append(YXYBB_interface_2)
        # YXYBB_datas.append(YXYBB_interface_3)
        # YXYBB_datas.append(YXYBB_interface_4)
        # YXYBB_datas.append(YXYBB_interface_5)
        # YXYBB_datas.append(YXYBB_interface_6)
        #
        # collection = Mongo.getInstance(table="statistical_item", ds='base').collection

        # YXYBB_interface_1_2 = statistical_item_BO.getInstance().set_project_name("YXYBB").set_statistical_type("interface").set_statistical_step(60 * 1).json2
        # print(YXYBB_interface_1_2)
        # print("AAAAAAAAAAAAAAA")
        # YXYBB_interface_1_2.pop("project_name")
        # print(YXYBB_interface_1_2)
        # print("BBBBBBBBBBBBBBBB")
        # YXYBB_interface_1_res = collection.find(YXYBB_interface_1_2)
        # for x in YXYBB_interface_1_res:
        #     print(x)
        # print("CCCCCCCCCCCCCCCC")
        # print(YXYBB_interface_1_res)
        # collection.insert_many(YXYBB_datas)
        pass

    def start(self):
        L.info("start sys , init DB_ds ")
        self.init_DB_ds()
        L.info("start sys , init statistical_item")
        self.statistical_item_init()
        L.info("start sys , compute all count data ")
        self.compute_count_all()


def getInstance():
    return DB_init()


if __name__ == "__main__":
    #DB_init().statistical_item_init()
    for i in range(3):
        statistical_step_datas = [i+1]
        DB_init().compute_step_infos(statistical_step_datas=statistical_step_datas)

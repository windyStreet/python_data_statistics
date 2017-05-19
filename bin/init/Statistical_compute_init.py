#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import threading
import queue
from bin.until import Mongo
from bin.until import Logger
from bin.until import DBCODE
from bin import logic
from bin.until import Filter
from bin.until import Time
from bin.logic.BO import statistic_res_BO
from bin.logic import BO
from bin.logic.BO import statistical_item_BO
import time
from bin.init import RabbitMQ_mongo_log

L = Logger.getInstance("times-task.log")


class Statistical_compute_init(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.step_type_count = 3
        self.queue = queue.Queue(self.step_type_count)
        self.thread_stop = False

    # 添加统计任务
    def add_item_compute_task(self):
        # 开启一个线程处理这个频率段的数据
        pass

    # 统计任务处理
    def statistical_deal(self, pars):
        while True:
            sleep_time = 60 * 60
            for par in pars:
                _id = par['_id']
                _item_mongo_instnce = Mongo.getInstance(table="statistical_item")
                _item_conllection = _item_mongo_instnce.getCollection()
                _item_bo = statistical_item_BO.getInstance()
                _item_bo.setId(_id)
                _item_filter = Filter.getInstance().filter("_id", _id, DBCODE.EQ)
                _item_info = _item_conllection.find_one(_item_filter.filter_json())

                statistical_step = _item_info['statistical_step']
                sleep_time = statistical_step * 60
                project_name = _item_info['project_name']
                statistical_type = _item_info['statistical_type']
                statistical_start_time = _item_info['statistical_start_time']
                times = Time.getComputeTimes(start_time=statistical_start_time, step=statistical_step)

                ds = logic.project_ds_info[project_name]
                table = project_name + "_" + statistical_type
                # 数据源数据，用于统计数据
                collection = Mongo.getInstance(table=table, ds=ds).collection

                documents = []
                lastTime = None
                L.debug("compute step is  %d s", statistical_step * 60)
                for i in range(1, len(times)):
                    lastTime = times[i]
                    _f = Filter.getInstance()
                    _f.filter("type", statistical_type, DBCODE.EQ)
                    _f.filter("project", project_name, DBCODE.EQ)
                    _f.filter("createtime", times[i - 1], DBCODE.GT)
                    _f.filter("createtime", times[i], DBCODE.LTE)
                    _filter = _f.filter_json()
                    count = collection.find(_filter).count()
                    document_bo = statistic_res_BO.getInstance()
                    document_bo.setStatistical_project(project_name)
                    document_bo.setStatistical_time(times[i])
                    document_bo.setStatistical_count(count)
                    document_bo.setStatistical_step(statistical_step)
                    document_bo.setStatistical_type(statistical_type)
                    documents.append(document_bo.json())
                    if len(documents) > 3000:
                        res_collection = Mongo.getInstance(table=BO.BASE_statistic_res).collection
                        res_collection.insert_many(documents=documents)  # 将结果插入到结果表中,防止爆了

                if len(documents) > 0:
                    res_collection = Mongo.getInstance(table=BO.BASE_statistic_res).collection
                    res_collection.insert_many(documents=documents)  # 将结果插入到结果表中
                else:
                    L.debug("statistical_deal ,not get the insert data")

                # 去更新statistical_item表
                if lastTime is not None:
                    _item_bo_1 = statistical_item_BO.getInstance()
                    _item_bo_1.setStatistical_start_time(lastTime)
                    _item_conllection.update_one(_item_filter.filter_json(), _item_bo_1.update_json)
                else:
                    L.debug("statistical_deal ,not get last time")

                #关闭数据库连接
                _item_mongo_instnce.close()
            L.debug("thread will sleep %s s", sleep_time)
            time.sleep(sleep_time)

    # 每一类分组启动一个线程进行处理任务
    def statistical_compute(self, pars=None):
        if pars is None:
            L.error("statistical_compute not given pars")
            return None
        t = threading.Thread(target=self.statistical_deal, args=(pars,))
        t.start()
        L.debug("statistical_compute,线程启动")
        pass

    def run(self):
        while not self.thread_stop:
            L.debug("thread%d %s: waiting for task" % (self.ident, self.name))
            try:
                task = self.queue.get(block=True, timeout=10)  # 接收消息 采用阻塞式 超时时间为10s
            except queue.Empty:
                L.debug("DB item task queue is empty")
                self.thread_stop = True
                break
            method = task['method']
            pars = task['pars']
            method(pars)  # 执行队列中的相关任务

            self.queue.task_done()  # 完成一个任务
            res = self.queue.qsize()  # 判断消息队列大小
            if res > 0:
                L.info("DB item have %d tasks to do", res)

    def stop(self):
        self.thread_stop = True

    def getTasks(self):
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

        if self.queue is None:
            L.error("task publish not the right queue")
            return None
        tasks = []
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
                task = {
                    "method": self.statistical_compute,
                    "pars": statistical_step_datas.copy()
                }
                tasks.append(task)
                statistical_step_min = statistical_step
                del statistical_step_datas[:]
                statistical_step_datas.append(statistical_data)
        task = {
            "method": self.statistical_compute,
            "pars": statistical_step_datas.copy()
        }
        tasks.append(task)
        return tasks

    # 队列的生产消费
    def product_consum(self):
        # 消息队列中无数据时，启动该线程，否则等待
        while True:
            try:
                msg_count = RabbitMQ_mongo_log.getInstance().getQueueMsgCount(queue="Mongodb_log")
                if msg_count == 0:
                    break
                time.sleep(5)
                L.debug("MQ remain have msg , the count is %d", msg_count)
                print("MQ remain have msg , the count is %d", msg_count)
            except Exception as e:
                L.warning(e)

        tasks = self.getTasks()  # 获取任务信息
        if tasks is not None:  # 初始化队列
            self.step_type_count = len(tasks)
            self.queue = queue.Queue(self.step_type_count)
        self.start()  # 启动队列
        for task in tasks:
            self.queue.put(task, block=True, timeout=None)  # 向队列中添加内容
        # self.queue.join()  # 等待所有任务完成
        L.info("item compute task add finished ")

    # 计算全部定时任务内容代码开始启动 (启动一个线程来进行处理)
    def start_init(self):
        t = threading.Thread(target=self.product_consum)
        t.start()


if __name__ == "__main__":
    # item_bo = statistical_item_BO.getInstance()
    # collection = Mongo.getInstance(table=BO.BASE_statistical_item).collection
    # datas = []
    # data_1 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(1).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_2 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(5).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_3 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(30).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_4 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(60).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_5 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(60*6).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_6 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(60*12).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # data_7 = item_bo.setProject_name("YXYBB").setStatistical_type("interface").setStatistical_step(60*24).setStatistical_start_time("2017-05-18 00:00:00.000").json
    # datas.append(data_1)
    # datas.append(data_2)
    # datas.append(data_3)
    # datas.append(data_4)
    # datas.append(data_5)
    # datas.append(data_6)
    # datas.append(data_7)
    # collection.insert_many(datas)
    #################################
    # Statistical_compute_init().start_init()
    pass

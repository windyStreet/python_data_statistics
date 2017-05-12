#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import threading
import queue
import time
from bin.until import Mongo
from bin.until import Logger
from bin.until import DBCODE
from bin import logic
from bin.until import Filter

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
            statistical_step = 60
            for par in pars:
                statistical_step = par['statistical_step']
                project_name = par['project_name']
                statistical_type = par['statistical_type']
                statistical_start_time = par['statistical_start_time']
                statistical_name = par['statistical_name']
                L.debug("sleep %d s", int(statistical_step / 10))
                ds = logic.project_ds_info[project_name]
                table = project_name + "_" + statistical_type

                collection = Mongo.getInstance(table=table, ds=ds).collection

                # _filter_infos = []
                # _filter = {"key": "name", "value": statistical_name, "relation": DBCODE.eq}
                # _filter = {"key": "project", "value": project_name, "relation": DBCODE.eq}
                # _filter = {"key": "type", "value": statistical_type, "relation": DBCODE.eq}
                # _filter = {"key": "createtime", "value": time_date, "relation": DBCODE.gt}
                # _filter = {"key": "createtime", "value": time_date, "relation": DBCODE.lt}

                _f = Filter.getInstance()
                _f.filter("type", statistical_type, DBCODE.eq)
                _f.filter("project", project_name, DBCODE.eq)
                _filter_datas = _f.filter_datas()
                print(_filter_datas)
                print("123456")
                # _filter_infos.append(_filter.copy())

                collection.find({})

                # 构造查询
                # 查询
                # 新增数据或者更新数据

            time.sleep(statistical_step * 60)
        pass

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
            print("thread%d %s: waiting for task" % (self.ident, self.name))
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

    # 计算全部定时任务内容代码开始启动 (启动一个线程来进行处理)
    def start_inti(self):
        t = threading.Thread(target=self.product_consum)
        t.start()

    # 队列的生产消费
    def product_consum(self):
        tasks = self.getTasks()  # 获取任务信息
        if tasks is not None:  # 初始化队列
            self.step_type_count = len(tasks)
            self.queue = queue.Queue(self.step_type_count)
        self.start()  # 启动队列
        for task in tasks:
            self.queue.put(task, block=True, timeout=None)  # 向队列中添加内容
        # self.queue.join()  # 等待所有任务完成
        L.info("item compute task add finished ")


if __name__ == "__main__":
    Statistical_compute_init().start_inti()
    pass

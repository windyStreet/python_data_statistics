#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime

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


class statistical_item_BO(object):
    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.updatetime = None
        self.project_name = None
        self.statistical_type = None
        self.statistical_start_time = None
        self.statistical_step = None
        self.statistical_name = None

    @property
    def json(self):
        """JSON format data."""
        json = {
            'createtime': self.createtime,
            'updatetime': self.updatetime,
            'project_name': self.project_name,
            'statistical_type': self.statistical_type,
            'statistical_start_time': self.statistical_start_time,
            'statistical_step': self.statistical_step,
            'statistical_name': self.statistical_name
        }
        json.update(self.kwargs)
        return json

    @property
    def json2(self):
        """JSON format data."""
        json2={}
        if self.updatetime is not None:
            json2['updatetime'] = self.updatetime
        if self.project_name is not None:
            json2['project_name'] = self.project_name
        if self.statistical_type is not None:
            json2['statistical_type'] = self.statistical_type
        if self.statistical_start_time is not None:
            json2['statistical_start_time'] = self.statistical_start_time
        if self.statistical_step is not None:
            json2['statistical_step'] = self.statistical_step
        if self.statistical_name is not None:
            json2['statistical_name'] = self.statistical_name
        json2.update(self.kwargs)
        return json2

    def set_statistical_name(self, statistical_name):
        self.statistical_name = statistical_name
        return self

    def get_statistical_name(self):
        return self.statistical_name

    def set_statistical_step(self, statistical_step):
        self.statistical_step = statistical_step
        return self

    def get_statistical_step(self):
        return self.statistical_step


    def statistical_start_time(self):
        return self.statistical_startTime

    def statistical_start_time(self, statistical_start_time):
        self.statistical_start_time = statistical_start_time
        return self

    def get_statistical_type(self):
        return self.statistical_type

    def set_statistical_type(self, statistical_type):
        self.statistical_type = statistical_type
        return self

    def get_project_name(self):
        return self.project_name

    def set_project_name(self, project_name):
        self.project_name = project_name
        return self

    def getCreatetime(self):
        return self.createtime

    def getUpdatetime(self):
        return self.updatetime

    def setCreatetime(self, createtime=None):
        if createtime is not None:
            self.createtime = createtime
        return self

    def setUpdateTime(self, updatetime=None):
        if updatetime is None:
            self.updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            self.updatetime = updatetime
        return self


def getInstance():
    return statistical_item_BO()

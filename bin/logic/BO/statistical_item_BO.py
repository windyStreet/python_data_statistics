#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime
from bin.until import DBCODE

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
    def __init__(self):
        self._id = None
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
        json = {}
        if self._id is not None:
            json['_id'] = self._id
        if self.updatetime is not None:
            json['updatetime'] = self.updatetime
        if self.project_name is not None:
            json['project_name'] = self.project_name
        if self.statistical_type is not None:
            json['statistical_type'] = self.statistical_type
        if self.statistical_start_time is not None:
            json['statistical_start_time'] = self.statistical_start_time
        if self.statistical_step is not None:
            json['statistical_step'] = self.statistical_step
        if self.statistical_name is not None:
            json['statistical_name'] = self.statistical_name
        return json

    @property
    def update_json(self):
        """JSON format data."""
        update_json = {DBCODE.RELATION_UPDATE: self.json}
        return update_json

    def setId(self, _id):
        self._id = _id
        return self

    def getId(self):
        return self._id;

    def setStatistical_name(self, statistical_name):
        self.statistical_name = statistical_name
        return self

    def getStatistical_name(self):
        return self.statistical_name

    def setStatistical_step(self, statistical_step):
        self.statistical_step = statistical_step
        return self

    def getStatistical_step(self):
        return self.statistical_step

    def getStatistical_start_time(self):
        return self.statistical_startTime

    def setStatistical_start_time(self, statistical_start_time):
        self.statistical_start_time = statistical_start_time
        return self

    def getStatistical_type(self):
        return self.statistical_type

    def setStatistical_type(self, statistical_type):
        self.statistical_type = statistical_type
        return self

    def getProject_name(self):
        return self.project_name

    def setProject_name(self, project_name):
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

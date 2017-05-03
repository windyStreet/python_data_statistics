#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime


class Statistics_OB(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.updatetime = None
        self.name = None
        self.type = None
        self.content = None

    @property
    def json(self):
        """JSON format data."""
        json = {
            'createtime': self.createtime,
            'updatetime': self.updatetime,
            'name': self.name,
            'type': self.type,
            'content': self.content
        }
        json.update(self.kwargs)
        return json

    def getCreatetime(self):
        return self.createtime

    def getUpdatetime(self):
        return self.updatetime

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getContent(self):
        return self.type

    def setCreatetime(self, createtime=None):
        if createtime is not None:
            self.createtime = createtime
        return self

    def setUpdateTime(self, updatetime=None):
        if updatetime is None:
            self.updatetime =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            self.updatetime = updatetime
        return self

    def setName(self, name=None):
        if name is not None:
            self.name = name
        return self

    def setType(self, type=None):
        if type is not None:
            self.type = type
        return self

    def setContent(self, content=None):
        if content is not None:
            self.content = content
        return self


def getInstance():
    return Statistics_OB()

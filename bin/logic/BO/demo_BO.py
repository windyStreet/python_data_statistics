#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import datetime


class demo_BO(object):
    '''
    statistical_item={
        "id":"主键",
        "createtime":"数据创建时间",
        "updatetime":"数据更新时间"
    }
    '''

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.updatetime = None

    @property
    def json(self):
        """JSON format data."""
        json = {
            'createtime': self.createtime,
            'updatetime': self.updatetime

        }
        json.update(self.kwargs)
        return json

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
    return demo_BO()

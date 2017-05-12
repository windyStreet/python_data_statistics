#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import DBCODE


class Filter(object):
    def __init__(self):
        self.key = None
        self.value = None
        self.relation = None
        self.filters = []

    @property
    def json(self):
        """JSON format data."""
        json = {
            'key': self.key,
            'value': self.value,
            'relation': self.relation,
        }
        json.update()
        return json

    def filter(self, key=None, value=None, relation=DBCODE.eq):
        self.key = key
        self.value = value
        self.relation = relation
        self.filters.append(self.json)
        return self

    def filter_datas(self):
        return self.filters

    # 构造生成 mongodb 查询条件json
    def filter_json(self):
        pass


def getInstance():
    return Filter()

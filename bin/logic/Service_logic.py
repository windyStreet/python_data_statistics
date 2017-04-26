#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import PR
from bin.until import Logger

L = Logger.getInstance()

class Service_logic(object):
    def logic(self, data):
        _PR = PR.getInstance()
        _data = {
            "title": {
                "text": 'ECharts 入门示例'
            },
            "tooltip": {
            },
            "legend": {
                "data": ['销量']
            },
            "xAxis": {
                "data": ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
            },
            "yAxis": {},
            "series": [{
                "name": '销量',
                "type": 'bar',
                "data": [5, 20, 36, 10, 10, 200]
            }]
        }
        _PR.setResult(_data)
        # L.debug(_data)
        # L.info(_data)
        # L.warn(_data)
        # L.error(_data)
        # L.critical(_data)
        return _PR.getPRBytes()

    def xx(self, data):
        print(data)
        return "abc"

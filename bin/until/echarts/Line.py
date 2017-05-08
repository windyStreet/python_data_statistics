#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import datetime
from bin.until import Logger

L = Logger.getInstance()


class Line(object):
    def __init__(self, collection, _legend_datas, _step, _step_count, _title_text, _type, _filter_others=[]):
        self._legend_datas = _legend_datas
        self._step_count = _step_count
        self._step = _step
        self.collection = collection
        self._title_text = _title_text
        self._type = _type
        self._filter_others = _filter_others

    def getLineChartData(self):
        series = []
        for _legend_data in self._legend_datas:
            series_data = []
            xAxis_data = []
            xAxis_data_x = []
            # datetime.strptime("2017-05-03 16:11", "%Y-%m-%d %H:%M:%S")
            _first_flag_time = datetime.datetime.now() - datetime.timedelta(minutes=self._step_count * self._step)
            for i in range(self._step_count):
                i += 1
                _xAxis = (_first_flag_time + datetime.timedelta(minutes=self._step * i))
                xAxis_data.append(_xAxis.strftime('%Y-%m-%d %H:%M'))
                xAxis_data_x.append(_xAxis)

            for _x_it in xAxis_data_x:
                _x_it_1 = (_x_it + datetime.timedelta(minutes=self._step)).strftime('%Y-%m-%d %H:%M:%S.%f')
                _x_it = _x_it.strftime('%Y-%m-%d %H:%M:%S.%f')
                _filter = \
                    {
                        "createtime":
                            {
                                "$gt": _x_it,
                                "$lt": _x_it_1
                            }
                    }
                for _filter_other in self._filter_others:
                    _filter[_filter_other["key"]] = _filter_other["value"]
                L.debug(_filter)
                L.debug(self.collection.find(_filter).count())
                series_data.append(self.collection.find(_filter).count())

                serie = {
                    "name": _legend_data,
                    "type": self._type,
                    "stack": '总量',
                    "data": series_data
                }
            series.append(serie)
        _result = {
            "title": {
                "text": self._title_text
            },
            "legend": {
                "data": self._legend_datas
            },
            "xAxis": {
                "data": xAxis_data
            },
            "series": series
        }
        return _result


def getInsatnce(collection, _legend_datas=None, _step=60, _step_count=7, _title_text="数据统计", _type="line", _filter_others=[]):
    if collection is None:
        L.warn("init Line  , not connection OBJ")
        return None
    if _legend_datas is None:
        L.warn("init Line  , not _legend_datas par")
        return None
    if _filter_others is None:
        L.warn("init Line  , not _filter_others par , will get all datas")
    return Line(collection, _legend_datas, _step, _step_count, _title_text, _type, _filter_others)

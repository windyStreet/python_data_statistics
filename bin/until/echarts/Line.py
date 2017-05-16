#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import datetime
from bin.until import Logger
from bin.until import Time
from bin.until import Mongo
from bin.until import DBCODE
from bin.until import Filter
from bin.logic import BO


L = Logger.getInstance()


class Line(object):
    # search_filter_infos = None, _step = 60, _step_count = 7, _title_text = "数据统计", _type = "line"
    def __init__(self, _search_filter_infos, _step, _step_count, _title_text, _type):
        self._search_filter_infos = _search_filter_infos
        self._step_count = _step_count
        self._step = _step
        self._title_text = _title_text
        self._type = _type

    def getFileter(self):
        pass

    def getLineChartData(self):
        series = []
        for key in self._search_filter_infos:
            _search_filter_info = self._search_filter_infos[key]
            _project = _search_filter_info['project_name']
            _filter_infos = _search_filter_info['filter_infos']

            now_str = Time.getNowStr()

            print(now_str)
            start_time = Time.getStartTime(step=self._step, step_count=self._step_count)
            times = Time.getComputeTimes(startTime=start_time, step=self._step)
            print(times)
            print(start_time)
            # 计划分批次查询

            res_collection = Mongo.getInstance(table=BO.BASE_statistic_res).collection
            res_filter = Filter.getInstance()
            res_filter.filter("statistical_time",times[0],DBCODE.GT)
            res_filter.filter("statistical_time",times[-2],DBCODE.LTE)
            res_filter.filter("statistical_step",self._step,DBCODE.EQ)
            res_filter.filter("statistical_project",_project,DBCODE.EQ)
            print(res_filter.filter_json())
            ress = res_collection.find(res_filter.filter_json())
            for res in ress:
                print(res)


            series_data = []
            xAxis_data = []
            xAxis_data_x = []

            _first_flag_time = datetime.datetime.now() - datetime.timedelta(minutes=self._step_count * self._step)
            for i in range(self._step_count):
                i += 1
                _xAxis = (_first_flag_time + datetime.timedelta(minutes=self._step * i))
                xAxis_data.append(_xAxis.strftime('%Y-%m-%d %H:%M'))
                xAxis_data_x.append(_xAxis)

            for _x_it in xAxis_data_x:
                _x_it_1 = (_x_it + datetime.timedelta(minutes=self._step)).strftime('%Y-%m-%d %H:%M:%S.%f')
                _x_it = _x_it.strftime('%Y-%m-%d %H:%M:%S.%f')

                # Time
                # _filter=getFileter(_search_filter_infos)
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


def getInsatnce(search_filter_infos=None, _step=60, _step_count=7, _title_text="数据统计", _type="line"):
    if search_filter_infos is None:
        L.warn("init Line  , not search_filter_infos par")
        return None
    return Line(search_filter_infos, _step, _step_count, _title_text, _type)

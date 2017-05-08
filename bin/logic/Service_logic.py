#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import PR
from bin.until import Logger
from echarts import Echart, Legend, Bar, Axis
from bin.until import Mongo
from bin.until.echarts import Line
from bin import logic

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
        print(_PR.getResult())
        # L.debug(_data)
        # L.info(_data)
        # L.warn(_data)
        # L.error(_data)
        # L.critical(_data)
        return _PR.getPRBytes()

    def xx(self, data):
        _PR = PR.getInstance()

        chart = Echart('GDP', 'This is a fake chart')
        chart.use(Bar('China', [2, 3, 4, 5]))
        chart.use(Legend(['GDP']))
        chart.use(Axis('category', 'bottom', data=['Nov', 'Dec', 'Jan', 'Feb']))
        _chart = chart.json
        print(_chart)
        _chart["tooltip"] = {}
        _PR.setResult(_chart)

        return _PR.getPRBytes()

    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    collection = Mongo.getInstance("statistics").collection

    # for i in range(20000):
    #    _data= Statistics_BO.getInstance().setName("YXYBB_click").setType("click").setContent("123").json
    #    collection.insert(_data)
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    # for it in collection.find({"name": "YXYBB_click"}):
    #    print(it)

    def line_test(self, data):
        collection = Mongo.getInstance("statistics").collection
        _PR = PR.getInstance()

        _title_text = data['title_text']  # 标题
        _step_count = data["step_count"]  # 横坐标点
        _step = data['step']  # 步长（单位:min）
        _type = data['type']  # 绘图类型
        _statistic_type = data['statistic_type']  # 统计类型
        _filter = data['filter']  # 统计类型

        __legend_infos = data['legend_infos']  # 数据项信息

        _legend_datas = __legend_infos.keys()  # 数据项名称
        _data_search_filter_info = {}
        for _legend_data in _legend_datas:
            _project_name = __legend_infos[_legend_data]['project_name']  # 项目名称
            # _project_id = __legend_infos[_legend_data]['project_id']#项目id
            ds = logic.project_ds_info[_project_name]  # 查询数据源
            table = _project_name + "_" + _statistic_type
            self_collection = Mongo.getInstance(table=table, ds=ds).collection
            _data_search_filter_info["_legend_data"] = {
                "self_collection": self_collection,  # 连接额外数据源
                "other_filter": [{"key": "type", "value": _statistic_type}]  # 过滤机制
            }
        # _filter_others = [{"key": "type", "value": _statistic_type}]

        # {"key": "name", "value": "YXYBB_click"}
        _result = Line.getInsatnce(collection=collection, _legend_datas=_legend_datas, _step=_step, _step_count=_step_count, _title_text=_title_text, _type=_type, _filter_others=_filter_others).getLineChartData()
        _PR.setResult(_result)
        return _PR.getPRBytes()

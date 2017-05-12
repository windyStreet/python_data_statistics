#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import PR
from bin.until import Logger
from echarts import Echart, Legend, Bar, Axis
from bin.until import Mongo
from bin.until.echarts import Line
from bin import logic
from bin.until import DBCODE

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
        # _statistic_type = data['statistic_type']  # 统计类型
        _filter_infos = data['filter_infos']  # 统计类型

        print(_filter_infos)
        # 保宝网的点击量和保宝网的观看人数统计的折线图 怎么处理？？？ 项目 类型
        _legend_infos = data['legend_infos']  # 数据项信息
        print(_legend_infos)
        _legend_datas = _legend_infos.keys()  # 数据项名称

        _search_filter_infos = {}
        for _legend_data in _legend_datas:
            _project_name = _legend_infos[_legend_data]['project_name']  # 项目名称
            # _project_id = __legend_infos[_legend_data]['project_id']#项目id
            _statistic_type = _legend_infos[_legend_data]['statistic_type']  # 项目id
            ds = logic.project_ds_info[_project_name]  # 查询数据源
            table = _project_name + "_" + _statistic_type
            self_collection = Mongo.getInstance(table=table, ds=ds).collection
            _filter_infos = []
            _filter = {"key": "type", "value": _statistic_type, "relation": DBCODE.eq}
            _filter_infos.append(_filter.copy())

            _search_filter_infos[_legend_data] = {
                "project_name": "_project_name",
                "self_collection": self_collection,  # 连接额外数据源
                "filter_infos": _filter_infos  # 过滤机制
            }

        # {"key": "name", "value": "YXYBB_click"}
        _result = Line.getInsatnce(search_filter_infos=_search_filter_infos, _step=_step, _step_count=_step_count, _title_text=_title_text, _type=_type).getLineChartData()
        _PR.setResult(_result)
        return _PR.getPRBytes()

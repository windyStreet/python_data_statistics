#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Mongo

ds_infos = Mongo.getInstance("project_ds").collection.find()
project_ds_info = {}
for ds_info in ds_infos:
    project_ds_info[ds_info["project"]] = ds_info["ds_code"]

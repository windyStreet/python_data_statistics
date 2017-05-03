#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import pymongo
from bin.until import Path
from bin.until import JsonFileFunc
import os

path = Path.getInstance().confDirPath + os.sep + "DB.json"
_db_info = JsonFileFunc.getInstance().readFile(path)
class Mongo(object):
    def __init__(self, table=None, ds=None,ip=None, port=None, dbname=None):
        if ds is None:
            ds = "base"
        if ip is None:
            ip = _db_info[ds]["ip"]
        if port is None:
            port = _db_info[ds]["port"]
        if dbname is None:
            dbname = _db_info[ds]["dbname"]
        if table is None:
            table = "default"
        user=_db_info[ds]["user"]
        password=_db_info[ds]["password"]
        client = pymongo.MongoClient(ip, port)
        dbname = client[dbname]
        self.collection = dbname[table]
        pass

def getInstance(table, ip=None, ds=None , port=None, dbname=None):
    return Mongo(table, ds,ip, port, dbname)


if __name__ == "__main__":
    print(pymongo.get_version_string())
    client = pymongo.MongoClient("192.168.7.216", 27017)
    db = client["echartdb"]
    collection = db["echart_collection"]
    print(collection.find().count())
    # collection.insert({"A":"aa","B":"bb"})
    # collection.insert({"A":"aa"})
    # collection.insert({"A1":"aa1","B1":"bb1"})
    # collection.insert({"C1":"cc1","B1":"bb1"})
    # collection.insert({"C1":"cc1","A1":"aa1"})
    # collection.insert({"C1":"cc1","A1":"aa"})
    # collection.insert({"C1":"cc1","A":"aa"})
    print(db.collection_names())
    print(str(collection.find()))
    print(str(collection.find().count()))
    print(str(collection.find({"A": "aa"})))
    print(collection.find_one())
    print("||||||||||||||||||||||")
    print(collection.find_one({"A": "aa"}))
    print("----------------------")
    print(collection.find({"A": "aa"}).count())
    for it in collection.find({"A": "aa"}):
        print(it)
    print("||||||||||||||||||||||")
    for item in collection.find():
        print(item)
    print("+++++++++++++++++++++++")
    for itts in collection.find().limit(5):
        print(itts)
    print("##################################")
    for itta in collection.find().sort("A", -1).limit(13):
        print(itta)
    print("**********************************")
    for ittb in collection.find().sort("B", -1).limit(10):
        print(ittb)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    for ittc in collection.find().skip(3).sort("B", -1).limit(10):
        print(ittc)
    print("((((((((((((((((((((((((((((((((((((")
    for ittd in collection.find().sort("A", -1).sort("B", -1).limit(13):
        print(ittd)
    print("))))))))))))))))))))))))))))))")
    for itte in collection.find().sort("A", -1).limit(13):
        print(itte)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for ittf in collection.find({"A1": {"$regex": "1"}}):
        print(ittf)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    for ittg in collection.find({"A1": "/?1?/"}):
        print(ittg)

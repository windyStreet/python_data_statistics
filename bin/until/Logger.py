#!/usr/bin/env python
# -*-  coding:utf-8 -*-

import logging
import logging.handlers
from bin.until import Path
import os

logPath = Path.getInstance().logsDirPath


class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        self.log_all = logPath + os.sep + "log.log"
        # formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        formatter = logging.Formatter('[%(levelname)8s]-[%(asctime)s]-%(filename)s :Line:%(lineno)d : %(message)s')
        # 日志文件名
        if filename is not None:
            self.filename = filename
            # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
            fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
            fh.suffix = "%Y%m%d-%H%M.log"
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)  # 定义handler的输出格式
            self.addHandler(fh)  # 给logger添加handler

        # # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh_all = logging.handlers.TimedRotatingFileHandler(self.log_all, 'M', 1, 30)
        fh_all.suffix = "%Y%m%d-%H%M.log"
        fh_all.setLevel(logging.DEBUG)
        fh_all.setFormatter(formatter)  # 定义handler的输出格式
        self.addHandler(fh_all)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)  # 定义handler的输出格式
        self.addHandler(ch)  # 给logger添加handler


def getInstance(filename=None):
    return Logger(filename)

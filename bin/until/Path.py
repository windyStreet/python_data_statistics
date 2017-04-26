#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import sys
import os

__author__ = 'windyStreet'
__time__ = '2017-03-17'


class Path(object):
    def __init__(self):
        self.path = sys.path[0]
        self.projectDirPath = self.path[0:self.path.rindex("bin")]
        self.confDirPath = self.projectDirPath + "conf" + os.sep
        self.binPath = self.projectDirPath + "bin" + os.sep
        self.logsDirPath = self.projectDirPath + "logs" + os.sep
        self.scriptsDirPath = self.projectDirPath + "scripts" + os.sep
        self.filesDirPath = self.projectDirPath + "files" + os.sep
        self.runtimeDirPath = self.projectDirPath + "runtime" + os.sep
        self.webPath = self.projectDirPath+"web"+os.sep
        self.htmlPath = self.webPath + "html" + os.sep
        self.javaScriptPath = self.webPath + "js" + os.sep
        self.cssPath = self.webPath + "css" + os.sep
        self.webPicPath = self.webPath + "pic" + os.sep
        pass


def getInstance():
    return Path()

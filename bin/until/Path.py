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
        self.confDirPath = self.projectDirPath + os.sep + "conf"
        self.binPath = self.projectDirPath + os.sep + "bin"
        self.logsDirPath = self.projectDirPath + os.sep + "logs"
        self.scriptsDirPath = self.projectDirPath + os.sep + "scripts"
        self.filesDirPath = self.projectDirPath + os.sep + "files"
        self.runtimeDirPath = self.projectDirPath + os.sep + "runtime"
        self.webPath = self.projectDirPath + os.sep + "web"
        self.htmlPath = self.webPath + os.sep + "html"
        self.javaScriptPath = self.webPath + os.sep + "js"
        self.cssPath = self.webPath + os.sep + "css"
        self.webPicPath = self.webPath + os.sep + "pic"
        pass


def getInstance():
    return Path()

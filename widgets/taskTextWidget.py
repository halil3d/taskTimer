#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui


class TaskTextWidgetBase(object):
    def getTaskName(self):
        error_msg = "getTaskName method must be implemented to "
        error_msg += "get the value of this widget as text."
        raise NotImplementedError(error_msg)


class TaskTextWidgetDefault(TaskTextWidgetBase, QtGui.QLineEdit):
    def getTaskName(self):
        return self.text()

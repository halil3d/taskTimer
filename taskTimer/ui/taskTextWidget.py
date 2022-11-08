#!/usr/bin/python
# -*- coding: utf-8 -*-
from qtpy import QtCore, QtGui, QtWidgets


class TaskTextWidgetBase(object):
    def serialise(self):
        error_msg = "serialise method must be implemented to "
        error_msg += "get the value of this widget as json data."
        raise NotImplementedError(error_msg)

    def deserialise(self, value):
            error_msg = "deserialise method must be implemented to "
            error_msg += "set the value of this widget from json data."
            raise NotImplementedError(error_msg)


class TaskTextWidgetDefault(TaskTextWidgetBase, QtWidgets.QLineEdit):
    def serialise(self):
        return self.text()

    def deserialise(self, value):
        self.setText(value)

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

import sys


if __name__ == "__main__" and __package__ is None:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from widgets.taskTimerWidget import TaskTimerWidget
app = QtGui.QApplication(sys.argv[1:])
t = TaskTimerWidget()
t.show()
sys.exit(app.exec_())

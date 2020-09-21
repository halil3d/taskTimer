#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

from taskTimerWidget import TaskTimerWidget

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimerWidget()
    t.show()
    sys.exit(app.exec_())

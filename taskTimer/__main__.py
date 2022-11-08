#!/usr/bin/python
# -*- coding: utf-8 -*-
from qtpy import QtCore, QtGui, QtWidgets

import sys

from taskTimer.ui.taskTimerWidget import TaskTimerWidget
app = QtWidgets.QApplication(sys.argv[1:])
t = TaskTimerWidget()
t.show()
sys.exit(app.exec_())

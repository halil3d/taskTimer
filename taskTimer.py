#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide import QtGui
import qtawesome
# from . import utils
import utils

# TODO: double click timer widget displays text edit for editing, enter to confirm
# cycle timer previous - Stop active timer if any and resume previous
# cycle timer next - Stop active timer if any and resume next


class TaskTimer(QtGui.QWidget):

    def __init__(self, *arg, **kwarg):
        super(self.__class__, self).__init__(*arg, **kwarg)
        self.totalTimerID = None

        self.listWidget = QtGui.QListWidget(self)
        self.totalTimeWidget = TimerWidget(self)
        # self.totalTimeLabel = QtGui.QLabel()
        self.newTaskButton = QtGui.QPushButton("+")
        self.removeTasksButton = QtGui.QPushButton("-")
        self.mergeTasksButton = QtGui.QPushButton("M")
        self.toggleTasksButton = QtGui.QPushButton("S/S")
        self.setupUI()

    def setupUI(self):
        self.newTaskButton.setFixedSize(36, 24)
        self.removeTasksButton.setFixedSize(36, 24)
        self.mergeTasksButton.setFixedSize(36, 24)
        self.toggleTasksButton.setFixedSize(36, 24)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        x, y, w, h = 100, 100, 350, 50
        self.setGeometry(x, y, w, h)

        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.mainLayout.addWidget(self.listWidget)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.totalTimeWidget)
        # self.buttonLayout.addWidget(self.totalTimeLabel)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.newTaskButton)
        self.buttonLayout.addWidget(self.removeTasksButton)
        self.buttonLayout.addWidget(self.mergeTasksButton)
        self.buttonLayout.addWidget(self.toggleTasksButton)

        self.newTaskButton.clicked.connect(self.addNewTask)
        self.removeTasksButton.clicked.connect(self.removeTasks)
        self.mergeTasksButton.clicked.connect(self.mergeTasks)
        self.toggleTasksButton.clicked.connect(self.toggleTasks)

    def addNewTask(self):
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            widget.stop()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(100, 50))
        newTask = TaskWidget()
        newTask.start()
        self.listWidget.setItemWidget(item, newTask)
        self.listWidget.addItem(item)
        if not self.totalTimerID:
            self.startTimer(1)

    def removeTasks(self):
        for item in self.listWidget.selectedItems():
            row = self.listWidget.row(item)
            item = self.listWidget.takeItem(row)
            del item

    def mergeTasks(self):
        elapsed = 0
        first_item = None
        for item in self.listWidget.selectedItems():
            if not first_item:
                first_item = item

            widget = self.listWidget.itemWidget(item)
            if widget.isActive():
                widget.stop()  # update elapsed
                widget.start()

            elapsed += widget.elapsed

            if item is not first_item:
                row = self.listWidget.row(item)
                item = self.listWidget.takeItem(row)
                del item

        widget = self.listWidget.itemWidget(first_item)
        widget.elapsed = elapsed

    def toggleTasks(self):
        for item in self.listWidget.selectedItems():
            widget = self.listWidget.itemWidget(item)
            widget.toggle()

    def timerEvent(self, event):
        totalElapsed = 0
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            totalElapsed += widget.elapsed
        self.totalTimeWidget.displayMilliseconds(totalElapsed)
        # seconds, remainder = divmod(totalElapsed, utils._timeMultiplier('secs', 'ms'))
        # if seconds:
        #     self.totalTimeLabel.setText(utils.timeToString(seconds, 'secs'))


class TaskWidget(QtGui.QWidget):
    def __init__(self, *arg, **kwarg):
        super(self.__class__, self).__init__(*arg, **kwarg)
        self.timerWidget = TimerWidget(self)
        self.taskLineEdit = QtGui.QLineEdit(self)
        bars = qtawesome.icon('fa5s.bars', color='green')
        pixmap = bars.pixmap(24, 24)
        self.moveLabel = QtGui.QLabel()
        self.moveLabel.setPixmap(pixmap)
        # self.stopButton = QtGui.QPushButton("S")
        # self.resetButton = QtGui.QPushButton("R")
        self.setupUI()

    def setupUI(self):
        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.timerWidget)
        self.mainLayout.addWidget(self.taskLineEdit)
        self.mainLayout.addWidget(self.moveLabel)
        # self.buttonLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addLayout(self.buttonLayout)

        # self.stopButton.setFixedSize(24, 24)
        # self.resetButton.setFixedSize(24, 24)
        # self.buttonLayout.addWidget(self.stopButton)
        # self.buttonLayout.addWidget(self.resetButton)

        # self.stopButton.clicked.connect(self.stop)
        # self.resetButton.clicked.connect(self.reset)

    @property
    def elapsed(self):
        return self.timerWidget.elapsed

    @elapsed.setter
    def elapsed(self, value):
        self.timerWidget.elapsed = value

    def isActive(self):
        return self.timerWidget.isActive()

    def start(self):
        self.timerWidget.start()

    def stop(self):
        self.timerWidget.stop()

    def reset(self):
        self.timerWidget.reset()

    def toggle(self):
        self.timerWidget.toggle()


class TimerWidget(QtGui.QLCDNumber):

    def __init__(self, parent=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.timerID = None
        self._elapsed = None
        self.timer = QtCore.QElapsedTimer()

        self.setDigitCount(8)
        self.setFixedHeight(24)
        self.setFixedWidth(120)

        self.reset()

    def isActive(self):
        if self.timerID:
            return True
        return False

    @property
    def elapsed(self):
        if self.timerID:
            return self._elapsed + self.timer.elapsed()
        else:
            return self._elapsed

    @elapsed.setter
    def elapsed(self, value):
        self._elapsed = value
        if not self.timerID:
            self.displayMilliseconds(value)

    def start(self):
        if not self.isActive():
            self.timerID = self.startTimer(1)
        self.timer.start()

    def stop(self):
        if self.timerID:
            self._elapsed += self.timer.elapsed()
            self.killTimer(self.timerID)
            self.timerID = None

    def reset(self):
        if self.timerID:
            self.killTimer(self.timerID)
            self.timerID = None

        self._elapsed = 0
        self.display("00:00:00")

    def toggle(self):
        if self.timerID:
            self.stop()
        else:
            self.start()

    def displayMilliseconds(self, milliseconds):
        days, remainder = divmod(milliseconds, utils._timeMultiplier('days', 'ms'))
        if days:
            raise Exception("Cannot set a value > 24 hours.")
        hours, remainder = divmod(remainder, utils._timeMultiplier('hours', 'ms'))
        minutes, remainder = divmod(remainder, utils._timeMultiplier('mins', 'ms'))
        seconds, remainder = divmod(remainder, utils._timeMultiplier('secs', 'ms'))
        timestring = '{:02.0f}:{:02.0f}:{:02.0f}'.format(hours, minutes, seconds)
        self.display(timestring)

    def timerEvent(self, event):
        milliseconds = self._elapsed + self.timer.elapsed()
        self.displayMilliseconds(milliseconds)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimer()
    t.show()
    sys.exit(app.exec_())

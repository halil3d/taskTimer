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
        self._totalTimerID = None
        self._mousePressed = None
        self._mousePosition = None

        self.listWidget = QtGui.QListWidget(self)
        self.totalTimeWidget = TimerWidget(self)
        # self.totalTimeLabel = QtGui.QLabel()
        self.roundHourButton = QtGui.QPushButton(qtawesome.icon('mdi.timelapse', 'mdi.numeric-1', 'mdi.alpha-h',
            options=[{
                'offset': (-0.2, 0)
            }, {
                'offset': (0.15, 0),
                'scale_factor': 1.5
            }, {
                'offset': (0.4, 0),
                'scale_factor': 1.5
            }]),
            "")
        self.round30MinsButton = QtGui.QPushButton(qtawesome.icon('mdi.timelapse'), "")
        self.closeButton = QtGui.QPushButton(qtawesome.icon('mdi.window-close'), "")
        self.newTaskButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-plus'), "")
        self.removeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-off'), "")
        self.mergeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-multiple'), "")
        self.toggleTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-snooze'), "")
        self.setupUI()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressed = True
            self._mousePosition = event.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self.move(self.mapToParent(event.pos() - self._mousePosition))

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressed = False
            self._mousePosition = None

    def setupUI(self):
        self.closeButton.setFixedSize(16, 16)
        self.closeButton.setFlat(True)

        self.newTaskButton.setFixedSize(36, 32)
        self.removeTasksButton.setFixedSize(36, 32)
        self.mergeTasksButton.setFixedSize(36, 32)
        self.toggleTasksButton.setFixedSize(36, 32)
        self.roundHourButton.setFixedSize(46, 32)
        self.roundHourButton.setIconSize(QtCore.QSize(30, 16))
        self.round30MinsButton.setFixedSize(36, 32)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        x, y, w, h = 100, 100, 500, 400
        self.setGeometry(x, y, w, h)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        sizegrip = QtGui.QSizeGrip(self)

        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.mainLayout.addWidget(self.closeButton, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
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
        self.buttonLayout.addWidget(self.roundHourButton)
        self.buttonLayout.addWidget(self.round30MinsButton)
        self.buttonLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.closeButton.clicked.connect(self.close)
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
        if not self._totalTimerID:
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
        bars = qtawesome.icon('mdi.drag')
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
        self._timerID = None
        self._elapsed = None
        self._timer = QtCore.QElapsedTimer()

        self.setupUI()
        self.reset()

    def setupUI(self):
        self.setDigitCount(8)
        self.setFixedHeight(24)
        self.setFixedWidth(120)
        self.setSegmentStyle(self.Flat)
        self.setStyleSheet("QLCDNumber{color: rgb(40, 180, 33); background-color: rgb(50, 70, 50);}")

    def isActive(self):
        if self._timerID:
            return True
        return False

    @property
    def elapsed(self):
        if self._timerID:
            return self._elapsed + self._timer.elapsed()
        else:
            return self._elapsed

    @elapsed.setter
    def elapsed(self, value):
        self._elapsed = value
        if not self._timerID:
            self.displayMilliseconds(value)

    def start(self):
        if not self.isActive():
            self._timerID = self.startTimer(1)
        self._timer.start()

    def stop(self):
        if self._timerID:
            self._elapsed += self._timer.elapsed()
            self.killTimer(self._timerID)
            self._timerID = None

    def reset(self):
        if self._timerID:
            self.killTimer(self._timerID)
            self._timerID = None

        self._elapsed = 0
        self.display("00:00:00")

    def toggle(self):
        if self._timerID:
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
        milliseconds = self._elapsed + self._timer.elapsed()
        self.displayMilliseconds(milliseconds)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimer()
    t.show()
    sys.exit(app.exec_())

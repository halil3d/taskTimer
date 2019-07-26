#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide import QtGui
from functools import partial
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
        self.roundHourButton = QtGui.QPushButton(
            qtawesome.icon(
                'mdi.timelapse',
                'mdi.numeric-1',
                'mdi.alpha-h',
                options=[{
                    'offset': (-0.2, 0)
                }, {
                    'offset': (0.15, 0),
                    'scale_factor': 1.5
                }, {
                    'offset': (0.4, 0),
                    'scale_factor': 1.5
                }]), "")
        self.round30MinsButton = QtGui.QPushButton(
            qtawesome.icon(
                'mdi.timelapse',
                'mdi.numeric-3',
                'mdi.numeric-0',
                'mdi.alpha-m',
                options=[{
                    'offset': (-0.35, 0)
                }, {
                    'offset': (-0.05, 0),
                    'scale_factor': 1.5
                }, {
                    'offset': (0.15, 0),
                    'scale_factor': 1.5
                }, {
                    'offset': (0.4, 0),
                    'scale_factor': 1.5
                }]), "")
        self.round15MinsButton = QtGui.QPushButton(
            qtawesome.icon(
                'mdi.timelapse',
                'mdi.numeric-1',
                'mdi.numeric-5',
                'mdi.alpha-m',
                options=[{
                    'offset': (-0.35, 0)
                }, {
                    'offset': (-0.05, 0),
                    'scale_factor': 1.5
                }, {
                    'offset': (0.15, 0),
                    'scale_factor': 1.5
                }, {
                    'offset': (0.4, 0),
                    'scale_factor': 1.5
                }]), "")
        self.closeButton = QtGui.QPushButton(qtawesome.icon('mdi.window-close'), "")
        self.newTaskButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-plus'), "")
        self.removeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-off'), "")
        self.mergeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-multiple'), "")
        self.toggleTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-snooze'), "")
        self.setupUI()

    def setupUI(self):
        self.closeButton.setFixedSize(16, 16)
        self.closeButton.setFlat(True)

        self.newTaskButton.setFixedSize(36, 32)
        self.removeTasksButton.setFixedSize(36, 32)
        self.mergeTasksButton.setFixedSize(36, 32)
        self.toggleTasksButton.setFixedSize(36, 32)
        self.roundHourButton.setFixedSize(46, 32)
        self.roundHourButton.setIconSize(QtCore.QSize(30, 16))
        self.round30MinsButton.setFixedSize(54, 32)
        self.round30MinsButton.setIconSize(QtCore.QSize(36, 16))
        self.round15MinsButton.setFixedSize(54, 32)
        self.round15MinsButton.setIconSize(QtCore.QSize(36, 16))

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
        self.buttonLayout.addWidget(self.round15MinsButton)
        self.buttonLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.closeButton.clicked.connect(self.close)
        self.newTaskButton.clicked.connect(self.addNewTask)
        self.removeTasksButton.clicked.connect(self.removeTasks)
        self.mergeTasksButton.clicked.connect(self.mergeTasks)
        self.toggleTasksButton.clicked.connect(self.toggleTasks)
        self.roundHourButton.clicked.connect(partial(self.roundUpOrAddTask, 60))
        self.round30MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 30))
        self.round15MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 15))

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Q:
                self.close()

        if event.key() == QtCore.Qt.Key_Equal:
            self.addNewTask()

        if event.key() == QtCore.Qt.Key_Minus:
            self.removeTasks()

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

    def addNewTask(self, elapsed=None):
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            widget.stop()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(100, 50))

        newTask = TaskWidget()
        if elapsed:
            newTask.setElapsed(elapsed)
        else:
            newTask.start()

        self.listWidget.setItemWidget(item, newTask)
        self.listWidget.addItem(item)
        if not self._totalTimerID:
            self.startTimer(1)

    def removeTasks(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            lastIndex = self.listWidget.count() - 1
            item = self.listWidget.item(lastIndex)
            selected = [item]

        for item in selected:
            row = self.listWidget.row(item)
            item = self.listWidget.takeItem(row)
            del item

    def mergeTasks(self):
        elapsed = 0
        first_item = None
        selected = self.listWidget.selectedItems()
        for item in selected:
            if not first_item:
                first_item = item

            widget = self.listWidget.itemWidget(item)
            if widget.isActive():
                widget.stop()  # update elapsed
                widget.start()

            elapsed += widget.elapsed()

            if item is not first_item:
                row = self.listWidget.row(item)
                item = self.listWidget.takeItem(row)
                del item

        widget = self.listWidget.itemWidget(first_item)
        widget.setElapsed(elapsed)

    def toggleTasks(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            lastIndex = self.listWidget.count() - 1
            item = self.listWidget.item(lastIndex)
            selected = [item]

        for item in selected:
            widget = self.listWidget.itemWidget(item)
            widget.toggle()

    def roundUpOrAddTask(self, minutes):
        selected = self.listWidget.selectedItems()
        if not selected:
            self.addNewTask(utils.convertTime(minutes, 'mins', 'ms'))
            return

        for item in selected:
            widget = self.listWidget.itemWidget(item)
            elapsed = widget.timerWidget.elapsed()
            elapsedBlock, roundUp = divmod(elapsed, minutes * utils._timeMultiplier('mins', 'ms'))
            if roundUp:
                elapsedBlock += 1

            widget.timerWidget.setElapsed(utils.convertTime(elapsedBlock * minutes, 'mins', 'ms'))

    def timerEvent(self, event):
        totalElapsed = 0
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            totalElapsed += widget.elapsed()
        self.totalTimeWidget.displayMilliseconds(totalElapsed)
        # seconds, remainder = divmod(totalElapsed, utils._timeMultiplier('secs', 'ms'))
        # if seconds:
        #     self.totalTimeLabel.setText(utils.timeToString(seconds, 'secs'))


class TaskWidget(QtGui.QWidget):
    def __init__(self, *arg, **kwarg):
        super(self.__class__, self).__init__(*arg, **kwarg)
        self.editElapsedWidget = QtGui.QLineEdit(self)
        self.editElapsedButton = QtGui.QPushButton(
            qtawesome.icon(
                'mdi.check',
                options=[{
                    'color': 'green'
                }]), "")
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

        self.editElapsedWidget.setFixedHeight(24)
        self.editElapsedWidget.setFixedWidth(80)
        self.editElapsedWidget.hide()
        self.editElapsedButton.hide()
        self.mainLayout.addWidget(self.editElapsedWidget)
        self.mainLayout.addWidget(self.editElapsedButton)
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

        self.editElapsedButton.clicked.connect(self.editElapsed)

    def elapsed(self):
        return self.timerWidget.elapsed()

    def setElapsed(self, value):
        self.timerWidget.setElapsed(value)

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

    def editElapsed(self):
        text = self.editElapsedWidget.text()
        if utils.isValidTimeString(text):
            elapsed = utils.stringToTime(text, 'ms')
            if elapsed:
                days, remainder = divmod(elapsed, utils._timeMultiplier('days', 'ms'))
                if not days:
                    self.setElapsed(elapsed)

        self.editElapsedWidget.setText("")
        self.editElapsedWidget.hide()
        self.editElapsedButton.hide()
        self.timerWidget.show()

    def mouseDoubleClickEvent(self, event):
        if self.childAt(event.pos()) == self.timerWidget:
            self.timerWidget.hide()
            self.editElapsedWidget.show()
            self.editElapsedWidget.setFocus()
            self.editElapsedButton.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if self.editElapsedWidget.hasFocus():
                self.editElapsedButton.click()


class TimerWidget(QtGui.QLCDNumber):

    def __init__(self, parent=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._timerID = None
        self._elapsed = 0
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

    def elapsed(self):
        if self._timerID:
            return self._elapsed + self._timer.elapsed()
        else:
            return self._elapsed

    def setElapsed(self, value):
        isActive = self.isActive()
        self.reset()
        self._elapsed = value
        if isActive:
            self.start()
        else:
            self.displayMilliseconds(value)

    def editable(self):
        return self._editable

    def setEditable(self, boolean):
        self._editable = boolean

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

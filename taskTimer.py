#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide import QtGui
from functools import partial
import qtawesome
# from . import utils
import utils


# TODO: Error handle time edit values with style/poup
# Add customisable tasktextwidget
# Add setToolTip methods of commit btn
# Add customisable commit button callback


class TaskTimer(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._totalTimerID = None
        self._mousePressed = None
        self._mousePosition = None

        self.listWidget = TaskListWidget(self)
        self.totalTimeWidget = TimerWidget(self)
        # self.totalTimeLabel = QtGui.QLabel()
        self.round15MinsIcon = qtawesome.icon(
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
            }])

        self.round30MinsIcon = qtawesome.icon(
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
            }])

        self.roundHourIcon = qtawesome.icon(
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
            }])

        self.roundHourButton = QtGui.QPushButton(self.roundHourIcon, "")
        self.round30MinsButton = QtGui.QPushButton(self.round30MinsIcon, "")
        self.round15MinsButton = QtGui.QPushButton(self.round15MinsIcon, "")
        self.minimizedButton = QtGui.QPushButton(qtawesome.icon('mdi.window-minimize'), "")
        self.closeButton = QtGui.QPushButton(qtawesome.icon('mdi.window-close'), "")
        self.newTaskButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-plus'), "")
        self.removeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-off'), "")
        self.mergeTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-multiple'), "")
        self.toggleTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.alarm-snooze'), "")
        self.commitTasksButton = QtGui.QPushButton(qtawesome.icon('mdi.cloud-upload'), "")
        self.setupUI()

    def setupUI(self):
        self.minimizedButton.setFixedSize(16, 16)
        self.minimizedButton.setFlat(True)
        self.closeButton.setFixedSize(16, 16)
        self.closeButton.setFlat(True)

        # self.newTaskButton.setFixedSize(36, 32)
        self.newTaskButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.mergeTasksButton.setFixedSize(36, 32)
        self.mergeTasksButton.setEnabled(False)
        self.removeTasksButton.setFixedSize(36, 32)
        self.removeTasksButton.setEnabled(False)
        # self.toggleTasksButton.setFixedSize(36, 32)
        self.toggleTasksButton.setEnabled(False)
        self.toggleTasksButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.roundHourButton.setFixedSize(46, 32)
        self.roundHourButton.setIconSize(QtCore.QSize(30, 16))
        self.roundHourButton.setEnabled(False)
        self.round30MinsButton.setFixedSize(54, 32)
        self.round30MinsButton.setIconSize(QtCore.QSize(36, 16))
        self.round30MinsButton.setEnabled(False)
        self.round15MinsButton.setFixedSize(54, 32)
        self.round15MinsButton.setIconSize(QtCore.QSize(36, 16))
        self.round15MinsButton.setEnabled(False)
        # self.commitTasksButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.commitTasksButton.setMinimumHeight(32)
        # self.commitTasksButton.setIconSize(QtCore.QSize(36, 32))

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        x, y, w, h = 100, 100, 500, 400
        self.setGeometry(x, y, w, h)
        self.setWindowTitle("Task Timer")
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        sizegrip = QtGui.QSizeGrip(self)

        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.windowIconLayout = QtGui.QHBoxLayout()
        self.windowIconLayout.addStretch()
        self.windowIconLayout.addWidget(self.minimizedButton)
        self.windowIconLayout.addWidget(self.closeButton)
        self.mainLayout.addLayout(self.windowIconLayout)

        self.mainLayout.addWidget(self.listWidget)
        self.topButtonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.topButtonLayout)
        self.topButtonLayout.addWidget(self.totalTimeWidget)
        # self.topButtonLayout.addWidget(self.totalTimeLabel)
        self.topButtonLayout.addStretch()
        self.topButtonLayout.addWidget(self.mergeTasksButton)
        self.topButtonLayout.addWidget(self.removeTasksButton)
        self.topButtonLayout.addWidget(self.roundHourButton)
        self.topButtonLayout.addWidget(self.round30MinsButton)
        self.topButtonLayout.addWidget(self.round15MinsButton)
        self.topButtonLayout.addWidget(self.commitTasksButton)

        self.middleButtonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.middleButtonLayout)
        self.middleButtonLayout.addWidget(self.newTaskButton)
        self.middleButtonLayout.addWidget(self.toggleTasksButton)
        self.middleButtonLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        # self.bottomButtonLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addLayout(self.bottomButtonLayout)
        # self.bottomButtonLayout.addWidget(self.commitTasksButton)
        # self.bottomButtonLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.minimizedButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)
        self.newTaskButton.clicked.connect(self.addTask)
        self.removeTasksButton.clicked.connect(self.removeTasks)
        self.mergeTasksButton.clicked.connect(self.mergeTasks)
        self.toggleTasksButton.clicked.connect(self.toggleTasks)
        self.roundHourButton.clicked.connect(partial(self.roundUpOrAddTask, 60))
        self.round30MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 30))
        self.round15MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 15))
        self.commitTasksButton.clicked.connect(self.commitTasks)
        self.listWidget.itemSelectionChanged.connect(self.changeButtonStates)

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Q:
                self.close()

        if event.key() == QtCore.Qt.Key_Equal:
            self.addTask()

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

    def addTask(self, elapsed=None):
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setSelected(False)
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

        self.changeButtonStates()

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

        self.changeButtonStates()

    def mergeTasks(self):
        elapsed = 0
        first_item = None
        selected = self.listWidget.selectedItems()
        if not selected:
            return

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

        self.changeButtonStates()

    def toggleTasks(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            lastIndex = self.listWidget.count() - 1
            item = self.listWidget.item(lastIndex)
            widget = self.listWidget.itemWidget(item)
            if not widget:
                return
            widget.toggle()
        else:
            if any([self.listWidget.itemWidget(item).isActive() for item in selected]):
                for item in selected:
                    widget = self.listWidget.itemWidget(item)
                    widget.stop()
            else:
                for item in selected:
                    widget = self.listWidget.itemWidget(item)
                    widget.start()

        self.changeButtonStates()

    def changeButtonStates(self):
        self.toggleTasksButton.setEnabled(True)
        self.removeTasksButton.setEnabled(True)
        self.mergeTasksButton.setEnabled(True)
        self.roundHourButton.setEnabled(True)
        self.round30MinsButton.setEnabled(True)
        self.round15MinsButton.setEnabled(True)
        selected = self.listWidget.selectedItems()

        if len(selected) < 1:
            self.mergeTasksButton.setEnabled(False)

            lastIndex = self.listWidget.count() - 1
            item = self.listWidget.item(lastIndex)

            if self.listWidget.itemWidget(item) is None:
                self.toggleTasksButton.setEnabled(False)
                self.removeTasksButton.setEnabled(False)
                self.roundHourButton.setEnabled(False)
                self.round30MinsButton.setEnabled(False)
                self.round15MinsButton.setEnabled(False)
                return

            selected = [item]

        elif len(selected) == 1:
            self.mergeTasksButton.setEnabled(False)
        elif len(selected) > 1:
            self.roundHourButton.setEnabled(False)
            self.round30MinsButton.setEnabled(False)
            self.round15MinsButton.setEnabled(False)

        if any([self.listWidget.itemWidget(x).isActive() for x in selected]):
            self.toggleTasksButton.setIcon(qtawesome.icon('mdi.alarm-snooze'))
        else:
            self.toggleTasksButton.setIcon(qtawesome.icon('mdi.alarm-check'))

    def roundUpOrAddTask(self, minutes, item=None):
        if item:
            selected = [item]
        else:
            selected = self.listWidget.selectedItems()

        if not selected:
            self.addTask(utils.convertTime(minutes, 'mins', 'ms'))
            return

        for item in selected:
            widget = self.listWidget.itemWidget(item)
            elapsed = widget.timerWidget.elapsed()
            elapsedBlock, roundUp = divmod(elapsed, minutes * utils._timeMultiplier('mins', 'ms'))
            if roundUp:
                elapsedBlock += 1

            widget.timerWidget.setElapsed(utils.convertTime(elapsedBlock * minutes, 'mins', 'ms'))

        self.changeButtonStates()

    def commitTasks(self):
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            print widget.taskLineEdit.text()
            print widget.elapsed()

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


class TaskListWidget(QtGui.QListWidget):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            menu = QtGui.QMenu(self)

            if not self.childAt(event.pos()).__class__ in [TaskWidget, TimerWidget]:
                action = QtGui.QAction(qtawesome.icon('mdi.alarm-check'), 'Add Task', self)
                action.activated.connect(self.parent().addTask)  # TBR: emit signal
                menu.addAction(action)

                presetsMenu = menu.addMenu(qtawesome.icon('mdi.menu'), 'Add Presets')
                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), '15mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 15))  # TBR: emit signal
                presetsMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), '30mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 30))  # TBR: emit signal
                presetsMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), '1hr', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 60))  # TBR: emit signal
                presetsMenu.addAction(action)
                menu.popup(self.mapToGlobal(event.pos()))
                return

            selected = self.selectedItems()
            if len(selected) <= 1:
                item = self.itemAt(event.pos())
                widget = self.itemWidget(item)
                if not widget:
                    return
                if widget.isActive():
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-snooze'), 'Pause Task', self)
                    action.activated.connect(widget.stop)  # TBR: emit signal
                    menu.addAction(action)
                else:
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-check'), 'Resume Task', self)
                    action.activated.connect(widget.start)  # TBR: emit signal
                    menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.circle-edit-outline'), 'Edit Task Time', self)
                action.activated.connect(widget.showEditElapsed)  # TBR: emit signal
                menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.alarm-off'), 'Remove Task', self)
                def _removeItem(item):
                    row = self.row(item)
                    item = self.takeItem(row)
                    del item
                action.activated.connect(partial(_removeItem, item))  # TBR: emit signal
                menu.addAction(action)

                roundUpMenu = menu.addMenu(qtawesome.icon('mdi.menu'), 'Round Up Time')
                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 15mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 15, item=self.itemAt(event.pos())))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 30mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 30, item=self.itemAt(event.pos())))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 1hr', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 60, item=self.itemAt(event.pos())))  # TBR: emit signal
                roundUpMenu.addAction(action)

            elif len(selected) > 1:
                if any([self.itemWidget(item).isActive() for item in selected]):
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-snooze'), 'Pause Tasks', self)
                    action.activated.connect(self.parent().toggleTasks)  # TBR: emit signal
                    menu.addAction(action)
                else:
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-check'), 'Resume Tasks', self)
                    action.activated.connect(self.parent().toggleTasks)  # TBR: emit signal
                    menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.alarm-multiple'), 'Merge Tasks', self)
                action.activated.connect(self.parent().mergeTasks)  # TBR: emit signal
                menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.alarm-off'), 'Remove Tasks', self)
                action.activated.connect(self.parent().removeTasks)  # TBR: emit signal
                menu.addAction(action)

                roundUpMenu = menu.addMenu(qtawesome.icon('mdi.menu'), 'Round Up Time')
                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 15mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 15))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 30mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 30))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 1hr', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 60))  # TBR: emit signal
                roundUpMenu.addAction(action)

            menu.popup(self.mapToGlobal(event.pos()))
            return

        super(self.__class__, self).mousePressEvent(event)

class TaskWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
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
            self.showEditElapsed()

    def showEditElapsed(self):
        self.timerWidget.hide()
        self.editElapsedWidget.show()
        self.editElapsedWidget.setFocus()
        self.editElapsedButton.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if self.editElapsedWidget.hasFocus():
                self.editElapsedButton.click()


class TimerWidget(QtGui.QLCDNumber):

    def __init__(self, parent=None, *argss, **kwargs):
        super(self.__class__, self).__init__(*argss, **kwargs)
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

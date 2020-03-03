#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from PySide import QtCore
from PySide import QtGui
from functools import partial
import qtawesome
# from . import utils
import utils


# TODO: Error handle time edit values with style/poup
# Add setToolTip methods of commit btn
# Add customisable commit button callback (add as option in commit button menu)
# Add export to csv option to commit button by default

class TaskTimer(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 taskTextWidget=None,
                 commitTasksCallback=None,
                 *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._totalTimerID = None
        self._mousePressed = None
        self._mousePosition = None
        self._taskTextWidget = taskTextWidget
        self._commitTasksCallback = commitTasksCallback
        self.taskSummary = None

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
        self.commitTasksButton.clicked.connect(self.commitTasksCallback)
        self.listWidget.itemSelectionChanged.connect(self.changeButtonStates)

    @property
    def taskTextWidget(self):
        return self._taskTextWidget

    @taskTextWidget.setter
    def taskTextWidget(self, taskTextWidget):
        self._taskTextWidget = taskTextWidget

    @property
    def commitTasksCallback(self):
        if not self._commitTasksCallback:
            self._commitTasksCallback = self.commitTasksDefault
        return self._commitTasksCallback

    @commitTasksCallback.setter
    def commitTasksCallback(self, commitTasksCallback):
        self._commitTasksCallback = commitTasksCallback

    def commitTasksDefault(self):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction(qtawesome.icon('mdi.file-document'), 'Export To CSV', self)
        action.activated.connect(self.exportTasksToCSV)
        menu.addAction(action)

        action = QtGui.QAction(qtawesome.icon('mdi.clipboard-text'), 'Show Summary', self)
        action.activated.connect(self.showTaskSummary)
        menu.addAction(action)

        p = self.sender().pos()
        menu.move(self.mapToParent(p).x(), self.mapToParent(p).y())
        menu.show()

    def exportTasksToCSV(self):
        pass

    def showTaskSummary(self):
        taskWidgets = self.getTaskWidgets()
        self.taskSummary = TaskSummary(self, taskWidgets=taskWidgets)
        self.taskSummary.show()

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
            taskWidget = self.listWidget.itemWidget(item)
            taskWidget.stop()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(100, 50))

        taskWidget = TaskWidget()
        if elapsed:
            taskWidget.setElapsed(elapsed)
        else:
            taskWidget.start()

        self.listWidget.setItemWidget(item, taskWidget)
        self.listWidget.addItem(item)
        if not self._totalTimerID:
            self.startTimer(1)

        self.changeButtonStates()
        taskWidget.taskTextWidget.setFocus()

    def removeTasks(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            lastIndex = self.listWidget.count() - 1
            taskItem = self.listWidget.item(lastIndex)
            selected = [taskItem]

        for taskItem in selected:
            row = self.listWidget.row(taskItem)
            taskItem = self.listWidget.takeItem(row)
            del taskItem

        self.changeButtonStates()

    def mergeTasks(self):
        elapsed = 0
        firstItem = None
        selected = self.listWidget.selectedItems()
        if not selected:
            return

        for taskItem in selected:
            if not firstItem:
                firstItem = taskItem

            taskWidget = self.listWidget.itemWidget(taskItem)
            if taskWidget.isActive():
                taskWidget.stop()  # update elapsed
                taskWidget.start()

            elapsed += taskWidget.elapsed()

            if taskItem is not firstItem:
                row = self.listWidget.row(taskItem)
                taskItem = self.listWidget.takeItem(row)
                del taskItem

        taskWidget = self.listWidget.itemWidget(firstItem)
        taskWidget.setElapsed(elapsed)

        self.changeButtonStates()

    def toggleTasks(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            lastIndex = self.listWidget.count() - 1
            taskItem = self.listWidget.item(lastIndex)
            taskWidget = self.listWidget.itemWidget(taskItem)
            if not taskWidget:
                return
            taskWidget.toggle()
        else:
            if any([self.listWidget.itemWidget(taskItem).isActive() for taskItem in selected]):
                for taskItem in selected:
                    taskWidget = self.listWidget.itemWidget(taskItem)
                    taskWidget.stop()
            else:
                for taskItem in selected:
                    taskWidget = self.listWidget.itemWidget(taskItem)
                    taskWidget.start()

        self.changeButtonStates()

    def getTaskWidgets(self):
        taskWidgets = []
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            taskWidget = self.listWidget.itemWidget(item)
            taskWidgets.append(taskWidget)

        return taskWidgets

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
            taskItem = self.listWidget.item(lastIndex)

            if self.listWidget.itemWidget(taskItem) is None:
                self.toggleTasksButton.setEnabled(False)
                self.removeTasksButton.setEnabled(False)
                self.roundHourButton.setEnabled(False)
                self.round30MinsButton.setEnabled(False)
                self.round15MinsButton.setEnabled(False)
                return

            selected = [taskItem]

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

    def roundUpOrAddTask(self, minutes, taskItem=None):
        if taskItem:
            selected = [taskItem]
        else:
            selected = self.listWidget.selectedItems()

        if not selected:
            self.addTask(utils.convertTime(minutes, 'mins', 'ms'))
            return

        for taskItem in selected:
            taskWidget = self.listWidget.itemWidget(taskItem)
            elapsed = taskWidget.timerWidget.elapsed()
            elapsedBlock, roundUp = divmod(elapsed, minutes * utils._timeMultiplier('mins', 'ms'))
            if roundUp:
                elapsedBlock += 1

            taskWidget.timerWidget.setElapsed(utils.convertTime(elapsedBlock * minutes, 'mins', 'ms'))

        self.changeButtonStates()

    def timerEvent(self, event):
        totalElapsed = 0
        for i in xrange(self.listWidget.count()):
            taskItem = self.listWidget.item(i)
            taskWidget = self.listWidget.itemWidget(taskItem)
            totalElapsed += taskWidget.elapsed()
        self.totalTimeWidget.displayMilliseconds(totalElapsed)
        # seconds, remainder = divmod(totalElapsed, utils._timeMultiplier('secs', 'ms'))
        # if seconds:
        #     self.totalTimeLabel.setText(utils.timeToString(seconds, inputUnit='secs'))


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
                taskItem = self.itemAt(event.pos())
                taskWidget = self.itemWidget(taskItem)
                if not taskWidget:
                    return
                if taskWidget.isActive():
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-snooze'), 'Pause Task', self)
                    action.activated.connect(taskWidget.stop)  # TBR: emit signal
                    menu.addAction(action)
                else:
                    action = QtGui.QAction(qtawesome.icon('mdi.alarm-check'), 'Resume Task', self)
                    action.activated.connect(taskWidget.start)  # TBR: emit signal
                    menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.circle-edit-outline'), 'Edit Task Time', self)
                action.activated.connect(taskWidget.showEditElapsed)  # TBR: emit signal
                menu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.alarm-off'), 'Remove Task', self)
                def _removeItem(taskItem):
                    row = self.row(taskItem)
                    taskItem = self.takeItem(row)
                    del taskItem
                action.activated.connect(partial(_removeItem, taskItem))  # TBR: emit signal
                menu.addAction(action)

                roundUpMenu = menu.addMenu(qtawesome.icon('mdi.menu'), 'Round Up Time')
                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 15mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 15, taskItem=self.itemAt(event.pos())))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 30mins', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 30, taskItem=self.itemAt(event.pos())))  # TBR: emit signal
                roundUpMenu.addAction(action)

                action = QtGui.QAction(qtawesome.icon('mdi.timelapse'), 'To 1hr', self)
                action.activated.connect(partial(self.parent().roundUpOrAddTask, 60, taskItem=self.itemAt(event.pos())))  # TBR: emit signal
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
    def __init__(self, parent=None, taskTextWidget=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.taskTextWidget = taskTextWidget

        self.editElapsedWidget = QtGui.QLineEdit(self)
        self.editElapsedButton = QtGui.QPushButton(
            qtawesome.icon(
                'mdi.check',
                options=[{
                    'color': 'green'
                }]), "")
        self.timerWidget = TimerWidget(self)
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
        self.mainLayout.addWidget(self.taskTextWidget)
        self.mainLayout.addWidget(self.moveLabel)
        # self.buttonLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addLayout(self.buttonLayout)

        # self.stopButton.setFixedSize(24, 24)
        # self.resetButton.setFixedSize(24, 24)
        # self.buttonLayout.addWidget(self.stopButton)
        # self.buttonLayout.addWidget(self.resetButton)

        # self.stopButton.clicked.connect(self.stop)
        # self.resetButton.clicked.connect(self.reset)

        # self.taskTextWidget.setFocus()

        self.editElapsedButton.clicked.connect(self.editElapsed)

    @property
    def taskTextWidget(self):
        """
        If a custom taskTextWidget is not set, use the default.
        """
        if not self._taskTextWidget:
            self._taskTextWidget = TaskTextWidgetDefault(self)
        return self._taskTextWidget

    @taskTextWidget.setter
    def taskTextWidget(self, taskTextWidget):
        if taskTextWidget is None:
            # No need to validate, default will be used
            pass
        elif not isinstance(taskTextWidget, TaskTextWidgetBase):
            print type(taskTextWidget)
            raise TypeError("taskTextwidget must be a subclass of TaskTextWidgetBase")
        self._taskTextWidget = taskTextWidget

    def getTaskName(self):
        return self.taskTextWidget.getTaskName()

    def elapsed(self):
        return self.timerWidget.elapsed()

    def setElapsed(self, value):
        self.timerWidget.setElapsed(value)

    def isActive(self):
        return self.timerWidget.isActive()

    def start(self):
        self.timerWidget.start()

    def started(self):
        return self.timerWidget.started()

    def stop(self):
        self.timerWidget.stop()

    def ended(self):
        return self.timerWidget.ended()

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
        self._started = None
        self._ended = None

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
        if not self._started:
            self._started = datetime.datetime.now()
        self._timer.start()

    def started(self):
        return self._started

    def stop(self):
        if self._timerID:
            self._elapsed += self._timer.elapsed()
            self.killTimer(self._timerID)
            self._timerID = None
            self._ended = datetime.datetime.now()

    def ended(self):
        if self._timerID:
            self._ended = datetime.datetime.now()
        return self._ended

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


class TaskSummary(QtGui.QWidget):
    def __init__(self, parent=None, taskWidgets=[], *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.taskWidgets = taskWidgets
        self._mousePressed = False
        self._mousePosition = None

        self.mainLayout = QtGui.QVBoxLayout(self)
        self.closeButton = QtGui.QPushButton(qtawesome.icon('mdi.window-close'), "")
        self.windowIconLayout = QtGui.QHBoxLayout()
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtGui.QTableView(self)

        self.setupUI()

    def setupUI(self):
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        x, y, w, h = 200, 200, 800, 300
        self.setGeometry(x, y, w, h)

        self.closeButton.setFixedSize(16, 16)
        self.closeButton.setFlat(True)

        self.setLayout(self.mainLayout)

        self.windowIconLayout.addStretch()
        self.windowIconLayout.addWidget(self.closeButton)
        self.mainLayout.addLayout(self.windowIconLayout)

        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.mainLayout.addWidget(self.tableView)

        sizegrip = QtGui.QSizeGrip(self)
        self.mainLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        headerRow = []
        for header in ["Task", "Start", "End", "Elapsed"]:
            headerRow.append(QtGui.QStandardItem(header))
        self.model.appendRow(headerRow)

        for taskWidget in self.taskWidgets:
            rowItems = [
                QtGui.QStandardItem(taskWidget.getTaskName()),
                QtGui.QStandardItem(taskWidget.started().strftime("%Y-%m-%d %H:%M:%S")),
                QtGui.QStandardItem(taskWidget.ended().strftime("%Y-%m-%d %H:%M:%S")),
                QtGui.QStandardItem(utils.timeToString(taskWidget.elapsed(), inputUnit='ms', minUnit='s'))
            ]
            self.model.appendRow(rowItems)

        self.tableView.setColumnWidth(0, 300)
        self.tableView.resizeColumnToContents(1)
        self.tableView.resizeColumnToContents(2)

        self.closeButton.clicked.connect(self.close)

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


class TaskTextWidgetBase(object):
    def getTaskName(self):
        error_msg = "getTaskName method must be implemented to "
        error_msg += "get the value of this widget as text."
        raise NotImplementedError(error_msg)


class TaskTextWidgetDefault(TaskTextWidgetBase, QtGui.QLineEdit):
    def getTaskName(self):
        return self.text()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimer()
    t.show()
    sys.exit(app.exec_())

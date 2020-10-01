#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
from functools import partial

import qtawesome
from PySide import QtCore, QtGui

from .taskListWidget import TaskListWidget
from .timerWidget import TimerWidget
from .taskWidget import TaskWidget
from .taskSummary import TaskSummary

from taskTimer import utils

# TODO: Change start/end time to added/updated as this is more accurate terminology
# TODO: Page up/down hotkeys for moving selected TaskWidget order in listview


class TaskTimerWidget(QtGui.QWidget):
    def __init__(self,
                 taskTextWidget=None,
                 exportTasksButtonCallback=None,
                 exportTasksCallback=None,
                 *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._totalTimerID = None
        self._mousePressed = None
        self._mousePosition = None
        self._taskTextWidget = taskTextWidget
        self._exportTasksButtonCallback = exportTasksButtonCallback
        self._exportTasksCallback = exportTasksCallback
        self.taskSummary = None
        self.listWidget = TaskListWidget(self)
        self.totalTimeWidget = TimerWidget(self)
        # self.totalTimeLabel = QtGui.QLabel()
        self.round15MinsIcon = qtawesome.icon(
            "mdi.timelapse",
            "mdi.numeric-1",
            "mdi.numeric-5",
            "mdi.alpha-m",
            options=[
                {"offset": (-0.35, 0)},
                {"offset": (-0.05, 0), "scale_factor": 1.5},
                {"offset": (0.15, 0), "scale_factor": 1.5},
                {"offset": (0.4, 0), "scale_factor": 1.5},
            ],
        )

        self.round30MinsIcon = qtawesome.icon(
            "mdi.timelapse",
            "mdi.numeric-3",
            "mdi.numeric-0",
            "mdi.alpha-m",
            options=[
                {"offset": (-0.35, 0)},
                {"offset": (-0.05, 0), "scale_factor": 1.5},
                {"offset": (0.15, 0), "scale_factor": 1.5},
                {"offset": (0.4, 0), "scale_factor": 1.5},
            ],
        )

        self.roundHourIcon = qtawesome.icon(
            "mdi.timelapse",
            "mdi.numeric-1",
            "mdi.alpha-h",
            options=[
                {"offset": (-0.2, 0)},
                {"offset": (0.15, 0), "scale_factor": 1.5},
                {"offset": (0.4, 0), "scale_factor": 1.5},
            ],
        )

        self.roundHourButton = QtGui.QPushButton(self.roundHourIcon, "")
        self.round30MinsButton = QtGui.QPushButton(self.round30MinsIcon, "")
        self.round15MinsButton = QtGui.QPushButton(self.round15MinsIcon, "")
        self.minimizedButton = QtGui.QPushButton(
            qtawesome.icon("mdi.window-minimize"), ""
        )
        self.closeButton = QtGui.QPushButton(qtawesome.icon("mdi.window-close"), "")
        self.newTaskButton = QtGui.QPushButton(qtawesome.icon("mdi.alarm-plus"), "")
        self.removeTasksButton = QtGui.QPushButton(qtawesome.icon("mdi.alarm-off"), "")
        self.mergeTasksButton = QtGui.QPushButton(
            qtawesome.icon("mdi.alarm-multiple"), ""
        )
        self.splitTaskButton = QtGui.QPushButton(qtawesome.icon("mdi.source-fork"), "")
        self.toggleTasksButton = QtGui.QPushButton(
            qtawesome.icon("mdi.alarm-snooze"), ""
        )
        self.exportTasksButton = QtGui.QPushButton(
            qtawesome.icon("mdi.cloud-upload"), ""
        )
        self.setupUI()

    def setupUI(self):

        self.minimizedButton.setFixedSize(16, 16)
        self.minimizedButton.setFlat(True)
        self.closeButton.setFixedSize(16, 16)
        self.closeButton.setFlat(True)

        # self.newTaskButton.setFixedSize(36, 32)
        self.newTaskButton.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed
        )
        self.newTaskButton.setToolTip("Add a new task\n(Ctrl + =/+)")
        self.mergeTasksButton.setFixedSize(36, 32)
        self.mergeTasksButton.setEnabled(False)
        self.mergeTasksButton.setToolTip("Merge selected tasks\n(M)")

        self.splitTaskButton.setFixedSize(36, 32)
        self.splitTaskButton.setEnabled(False)
        self.splitTaskButton.setToolTip("Split selected task\n(S)")

        self.removeTasksButton.setFixedSize(36, 32)
        self.removeTasksButton.setEnabled(False)
        self.removeTasksButton.setToolTip(
            "Remove selected task\n-- or --\nRemove last task\n(Ctrl + -)"
        )
        # self.toggleTasksButton.setFixedSize(36, 32)
        self.toggleTasksButton.setEnabled(False)
        self.toggleTasksButton.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed
        )
        self.toggleTasksButton.setToolTip(
            "Pause / Resume selected tasks\n"
            "-- or --\n"
            "Pause / Resume last task\n"
            "(Return)"
        )
        self.roundHourButton.setFixedSize(46, 32)
        self.roundHourButton.setIconSize(QtCore.QSize(30, 16))
        self.roundHourButton.setEnabled(True)
        self.roundHourButton.setToolTip(
            "Add a new task with 1 hour preset\n"
            "-- or --\n"
            "Round selected to nearest hour\n"
            "(Ctrl + 1)"
        )
        self.round30MinsButton.setFixedSize(54, 32)
        self.round30MinsButton.setIconSize(QtCore.QSize(36, 16))
        self.round30MinsButton.setEnabled(True)
        self.round30MinsButton.setToolTip(
            "Add a new task with 30 minute preset\n"
            "-- or --\n"
            "Round selected to nearest 30 minutes\n"
            "(Ctrl + 2)"
        )
        self.round15MinsButton.setFixedSize(54, 32)
        self.round15MinsButton.setIconSize(QtCore.QSize(36, 16))
        self.round15MinsButton.setEnabled(True)
        self.round15MinsButton.setToolTip(
            "Add a new task with 15 minute preset\n"
            "-- or --\n"
            "Round selected to nearest 15 minutes\n"
            "Ctrl + 3"
        )
        # self.exportTasksButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.exportTasksButton.setMinimumHeight(32)
        # self.exportTasksButton.setIconSize(QtCore.QSize(36, 32))
        self.exportTasksButton.setToolTip(
            "Show Tasks Summary\n"
            "-- or --\n"
            "Export Tasks Summary\n"
            "(Ctrl + E)"
        )

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        x, y, w, h = 700, 300, 500, 400
        self.setGeometry(x, y, w, h)
        screen = QtGui.QDesktopWidget().screenGeometry()
        x_offset, y_offset = (0, 0)
        if sys.platform == 'win32':
            y_offset = 50
        self.move(screen.width() - w - x_offset, screen.height() - h - y_offset)

        self.setWindowTitle("Task Timer")
        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
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
        self.topButtonLayout.addWidget(self.splitTaskButton)
        self.topButtonLayout.addWidget(self.mergeTasksButton)
        self.topButtonLayout.addWidget(self.removeTasksButton)
        self.topButtonLayout.addWidget(self.roundHourButton)
        self.topButtonLayout.addWidget(self.round30MinsButton)
        self.topButtonLayout.addWidget(self.round15MinsButton)
        self.topButtonLayout.addWidget(self.exportTasksButton)

        self.middleButtonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.middleButtonLayout)
        self.middleButtonLayout.addWidget(self.newTaskButton)
        self.middleButtonLayout.addWidget(self.toggleTasksButton)
        self.middleButtonLayout.addWidget(
            sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
        )

        # self.bottomButtonLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addLayout(self.bottomButtonLayout)
        # self.bottomButtonLayout.addWidget(self.exportTasksButton)
        # self.bottomButtonLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        # Button connections
        self.minimizedButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)
        self.newTaskButton.clicked.connect(self.addTask)
        self.removeTasksButton.clicked.connect(self.removeTasks)
        self.mergeTasksButton.clicked.connect(self.mergeTasks)
        self.splitTaskButton.clicked.connect(self.splitTask)
        self.toggleTasksButton.clicked.connect(self.toggleTasks)
        self.roundHourButton.clicked.connect(partial(self.roundUpOrAddTask, 60))
        self.round30MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 30))
        self.round15MinsButton.clicked.connect(partial(self.roundUpOrAddTask, 15))
        self.exportTasksButton.clicked.connect(self.exportTasksButtonCallback)
        self.listWidget.itemSelectionChanged.connect(self.updateButtonStates)

        # Signal connections
        self.listWidget.addTaskSignal.connect(self.addTask)
        self.listWidget.roundUpOrAddTaskSignal.connect(self.roundUpOrAddTask)
        self.listWidget.toggleTasksSignal.connect(self.toggleTasks)
        self.listWidget.mergeTasksSignal.connect(self.mergeTasks)
        self.listWidget.removeTasksSignal.connect(self.removeTasks)
        self.listWidget.updateButtonStatesSignal.connect(self.updateButtonStates)

    @property
    def taskTextWidget(self):
        return self._taskTextWidget

    @taskTextWidget.setter
    def taskTextWidget(self, taskTextWidget):
        self._taskTextWidget = taskTextWidget

    @property
    def exportTasksButtonCallback(self):
        if not self._exportTasksButtonCallback:
            self._exportTasksButtonCallback = self.exportTasksButtonDefault
        return self._exportTasksButtonCallback

    @exportTasksButtonCallback.setter
    def exportTasksButtonCallback(self, exportTasksButtonCallback):
        self._exportTasksButtonCallback = exportTasksButtonCallback

    @property
    def exportTasksCallback(self):
        if not self._exportTasksCallback:
            self._exportTasksCallback = self.exportTasksToCSV
        return self._exportTasksCallback

    @exportTasksCallback.setter
    def exportTasksCallback(self, exportTasksCallback):
        self._exportTasksCallback = exportTasksCallback

    def exportTasksButtonDefault(self):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction(
            qtawesome.icon("mdi.file-document"), "&Export To CSV", self
        )
        action.activated.connect(self.exportTasksToCSV)
        menu.addAction(action)

        action = QtGui.QAction(
            qtawesome.icon("mdi.file-document"), "&Load From CSV", self
        )
        action.activated.connect(self.loadTasksFromCSV)
        menu.addAction(action)

        action = QtGui.QAction(
            qtawesome.icon("mdi.clipboard-text"), "&Show Summary", self
        )
        action.activated.connect(self.showTaskSummary)
        menu.addAction(action)

        menu.show()
        p = self.exportTasksButton.pos()
        menu.move(self.mapToParent(p).x() - menu.rect().width(), self.mapToParent(p).y())

    def exportTasksToCSV(self):
        import os
        import csv
        import time

        d = datetime.datetime.fromtimestamp(time.time())

        csv_file = os.path.expanduser(
            "~/.taskTimer/%s_tasktimer.csv" % (d.strftime("%Y-%m-%d_%H%M%S"))
        )
        if not os.path.exists(os.path.dirname(csv_file)):
            os.makedirs(os.path.dirname(csv_file))

        taskWidgets = self.getTaskWidgets()

        with open(csv_file, "wb") as csvfile:
            header = ["Task", "Start", "End", "Elapsed"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            for taskWidget in taskWidgets:
                writer.writerow(
                    taskWidget.serialise()
                )

        QtGui.QMessageBox.information(
            self, "Export Tasks To CSV", "CSV File Created:\n%s" % csv_file
        )

    def loadTasksFromCSV(self):
        import os
        import csv

        csvDir = os.path.expanduser("~/.taskTimer")
        selectData = QtGui.QFileDialog.getOpenFileName(self,
            "Open Saved Data", csvDir, "CSV Files (*.csv)")
        csvPath = selectData[0]
        if not csvPath:
            return

        with open(csvPath) as csvFile:
            reader = csv.DictReader(csvFile)
            for taskData in reader:
                item = QtGui.QListWidgetItem(self.listWidget)
                item.setSizeHint(QtCore.QSize(100, 50))

                taskWidget = TaskWidget.fromData(taskData, taskTextWidget=self.taskTextWidget)
                taskWidget.addTaskSignal.connect(self.addTask)

                self.listWidget.setItemWidget(item, taskWidget)
                self.listWidget.addItem(item)

        self.updateButtonStates()

    def showTaskSummary(self):
        taskWidgets = self.getTaskWidgets()
        self.taskSummary = TaskSummary(taskWidgets=taskWidgets)
        self.taskSummary.show()

    def keyPressEvent(self, event):
        # Quit
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Q:
                self.close()

            if event.key() == QtCore.Qt.Key_1:
                self.roundUpOrAddTask(60)

            if event.key() == QtCore.Qt.Key_2:
                self.roundUpOrAddTask(30)

            if event.key() == QtCore.Qt.Key_3:
                self.roundUpOrAddTask(15)

            if event.key() == QtCore.Qt.Key_E:
                self.exportTasksButtonCallback()

        # Add new Task
        if event.key() in [QtCore.Qt.Key_Equal, QtCore.Qt.Key_Plus]:
            self.addTask()

        # Remove Task(s)
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

        taskWidget = TaskWidget(taskTextWidget=self.taskTextWidget)
        taskWidget.addTaskSignal.connect(self.addTask)
        if elapsed:
            taskWidget.setElapsed(elapsed)
            taskWidget.stop()
        else:
            taskWidget.start()

        self.listWidget.setItemWidget(item, taskWidget)
        self.listWidget.addItem(item)
        if not self._totalTimerID:
            self.startTimer(1)

        self.updateButtonStates()
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

        self.updateButtonStates()

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

        self.updateButtonStates()

    def splitTask(self):
        selected = self.listWidget.selectedItems()
        if not selected:
            return

        taskItem = selected[-1]
        taskWidget = self.listWidget.itemWidget(taskItem)
        taskWidget.showEditElapsed(split=True)

        self.updateButtonStates()

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
            if any(
                [
                    self.listWidget.itemWidget(taskItem).isActive()
                    for taskItem in selected
                ]
            ):
                for taskItem in selected:
                    taskWidget = self.listWidget.itemWidget(taskItem)
                    taskWidget.stop()
            else:
                for taskItem in selected:
                    taskWidget = self.listWidget.itemWidget(taskItem)
                    taskWidget.start()

        self.updateButtonStates()

    def getTaskWidgets(self):
        taskWidgets = []
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            taskWidget = self.listWidget.itemWidget(item)
            taskWidgets.append(taskWidget)

        return taskWidgets

    def updateButtonStates(self):
        self.toggleTasksButton.setEnabled(True)
        self.removeTasksButton.setEnabled(True)
        self.mergeTasksButton.setEnabled(True)
        self.splitTaskButton.setEnabled(True)
        self.roundHourButton.setEnabled(True)
        self.round30MinsButton.setEnabled(True)
        self.round15MinsButton.setEnabled(True)
        selected = self.listWidget.selectedItems()

        if len(selected) < 1:
            self.mergeTasksButton.setEnabled(False)
            self.splitTaskButton.setEnabled(False)

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
            self.toggleTasksButton.setIcon(qtawesome.icon("mdi.alarm-snooze"))
        else:
            self.toggleTasksButton.setIcon(qtawesome.icon("mdi.alarm-check"))

    def roundUpOrAddTask(self, minutes, taskItem=None):
        if taskItem:
            selected = [taskItem]
        else:
            selected = self.listWidget.selectedItems()

        if not selected:
            self.addTask(utils.convertTime(minutes, "mins", "ms"))
            return

        for taskItem in selected:
            taskWidget = self.listWidget.itemWidget(taskItem)
            elapsed = taskWidget.timerWidget.elapsed()
            elapsedBlock, roundUp = divmod(
                elapsed, minutes * utils.timeMultiplier("mins", "ms")
            )
            if roundUp:
                elapsedBlock += 1

            taskWidget.timerWidget.setElapsed(
                utils.convertTime(elapsedBlock * minutes, "mins", "ms")
            )

        self.updateButtonStates()

    def timerEvent(self, event):
        totalElapsed = 0
        for i in xrange(self.listWidget.count()):
            taskItem = self.listWidget.item(i)
            taskWidget = self.listWidget.itemWidget(taskItem)
            totalElapsed += taskWidget.elapsed()
        self.totalTimeWidget.displayMilliseconds(totalElapsed)
        # seconds, remainder = divmod(totalElapsed, utils.timeMultiplier('secs', 'ms'))
        # if seconds:
        #     self.totalTimeLabel.setText(utils.timeToString(seconds, inputUnit='secs'))

    def close(self):
        """
        I always rush to shutdown and close everything after finishing work,
        and always forget to save all the hard work I've logged.
        This will ensure a nagging popup makes me think twice.
        """
        if self.listWidget.count():
            activeTimers = False
            for i in xrange(self.listWidget.count()):
                item = self.listWidget.item(i)
                taskWidget = self.listWidget.itemWidget(item)
                if taskWidget.isActive():
                    activeTimers = True
                    break

            title = "Are you sure you want to quit?"
            if activeTimers:
                text = "There are timers that are currently active."
                text += "\n\nExport and Quit to record your progress. "
                text += "\nQuit to discard them, or Cancel to return."
            else:
                text = "Export and Quit to record your progress."
                text += "\nQuit to discard, or Cancel to return."

            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(title)
            msgBox.setText(text)
            msgBox.setIcon(QtGui.QMessageBox.Question)
            exportAndQuitButton = msgBox.addButton(
                "&Export and Quit", QtGui.QMessageBox.AcceptRole)
            quitButton = msgBox.addButton(
                "&Quit", QtGui.QMessageBox.DestructiveRole)
            cancelButton = msgBox.addButton(
                "&Cancel", QtGui.QMessageBox.RejectRole)

            msgBox.setDefaultButton(cancelButton)

            msgBox.exec_()

            selectedButton = msgBox.clickedButton()
            role = msgBox.buttonRole(selectedButton)
            if role == QtGui.QMessageBox.AcceptRole:
                self.exportTasksCallback()
                super(self.__class__, self).close()
            elif role == QtGui.QMessageBox.DestructiveRole:
                super(self.__class__, self).close()
            elif role == QtGui.QMessageBox.RejectRole:
                return

        super(self.__class__, self).close()

#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from functools import partial

import qtawesome
from qtpy import QtCore, QtGui, QtWidgets

from taskTimer.ui.timerWidget import TimerWidget
from taskTimer.ui.taskWidget import TaskWidget


class TaskListWidget(QtWidgets.QListWidget):
    addTaskSignal = QtCore.Signal(int)
    roundUpOrAddTaskSignal = QtCore.Signal(int)
    toggleTasksSignal = QtCore.Signal()
    mergeTasksSignal = QtCore.Signal()
    removeTasksSignal = QtCore.Signal()
    updateButtonStatesSignal = QtCore.Signal()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            menu = QtWidgets.QMenu(self)

            if not self.childAt(event.pos()).__class__ in [TaskWidget, TimerWidget]:
                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.alarm-check"), "Add Task", self
                )
                action.activated.connect(partial(self.addTaskSignal.emit, None))
                menu.addAction(action)

                presetsMenu = menu.addMenu(qtawesome.icon("mdi.menu"), "Add Presets")
                action = QtWidgets.QAction(qtawesome.icon("mdi.timelapse"), "15mins", self)
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 15))
                presetsMenu.addAction(action)

                action = QtWidgets.QAction(qtawesome.icon("mdi.timelapse"), "30mins", self)
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 30))
                presetsMenu.addAction(action)

                action = QtWidgets.QAction(qtawesome.icon("mdi.timelapse"), "1hr", self)
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 60))
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
                    action = QtWidgets.QAction(
                        qtawesome.icon("mdi.alarm-snooze"), "Pause Task", self
                    )
                    action.activated.connect(taskWidget.stop)
                    menu.addAction(action)
                else:
                    action = QtWidgets.QAction(
                        qtawesome.icon("mdi.alarm-check"), "Resume Task", self
                    )
                    action.activated.connect(taskWidget.start)
                    menu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.circle-edit-outline"), "Edit Task Time", self
                )
                action.activated.connect(taskWidget.showEditElapsed)
                menu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.source-fork"), "Split Task Time", self
                )
                action.activated.connect(partial(taskWidget.showEditElapsed, True))
                menu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.alarm-off"), "Remove Task", self
                )

                def _removeItem(taskItem):
                    row = self.row(taskItem)
                    taskItem = self.takeItem(row)
                    del taskItem

                action.activated.connect(partial(_removeItem, taskItem))
                menu.addAction(action)

                roundUpMenu = menu.addMenu(qtawesome.icon("mdi.menu"), "Round Up Time")
                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.timelapse"), "To 15mins", self
                )
                action.activated.connect(
                    partial(
                        self.roundUpOrAddTaskSignal.emit,
                        15
                    )
                )
                roundUpMenu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.timelapse"), "To 30mins", self
                )
                action.activated.connect(
                    partial(
                        self.roundUpOrAddTaskSignal.emit,
                        30
                    )
                )
                roundUpMenu.addAction(action)

                action = QtWidgets.QAction(qtawesome.icon("mdi.timelapse"), "To 1hr", self)
                action.activated.connect(
                    partial(
                        self.roundUpOrAddTaskSignal.emit,
                        60
                    )
                )
                roundUpMenu.addAction(action)

            elif len(selected) > 1:
                if any([self.itemWidget(item).isActive() for item in selected]):
                    action = QtWidgets.QAction(
                        qtawesome.icon("mdi.alarm-snooze"), "Pause Tasks", self
                    )
                    action.activated.connect(self.toggleTasksSignal.emit)
                    menu.addAction(action)
                else:
                    action = QtWidgets.QAction(
                        qtawesome.icon("mdi.alarm-check"), "Resume Tasks", self
                    )
                    action.activated.connect(self.toggleTasksSignal.emit)
                    menu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.alarm-multiple"), "Merge Tasks", self
                )
                action.activated.connect(self.mergeTasksSignal.emit)
                menu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.alarm-off"), "Remove Tasks", self
                )
                action.activated.connect(self.removeTasksSignal.emit)
                menu.addAction(action)

                roundUpMenu = menu.addMenu(qtawesome.icon("mdi.menu"), "Round Up Time")
                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.timelapse"), "To 15mins", self
                )
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 15))
                roundUpMenu.addAction(action)

                action = QtWidgets.QAction(
                    qtawesome.icon("mdi.timelapse"), "To 30mins", self
                )
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 30))
                roundUpMenu.addAction(action)

                action = QtWidgets.QAction(qtawesome.icon("mdi.timelapse"), "To 1hr", self)
                action.activated.connect(partial(self.roundUpOrAddTaskSignal.emit, 60))
                roundUpMenu.addAction(action)

            menu.popup(self.mapToGlobal(event.pos()))
            return

        super(self.__class__, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        propagate_event = True
        selected = self.selectedItems()

        if selected:
            # Merge Selected Tasks
            if event.key() == QtCore.Qt.Key_M:
                self.mergeTasksSignal.emit()

            if event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                # Move Tasks Up
                if event.key() == QtCore.Qt.Key_Up:
                    propagate_event = False
                    self.moveTasksUp()

                # Move Tasks Down
                if event.key() == QtCore.Qt.Key_Down:
                    propagate_event = False
                    self.moveTasksDown()

            for i, taskItem in enumerate(selected, start=1):
                taskWidget = self.itemWidget(taskItem)
                if i == len(selected):
                    # Edit Elapsed
                    if event.key() == QtCore.Qt.Key_E:
                        if not taskWidget.taskTextWidget.hasFocus():
                            taskWidget.showEditElapsed()
                    # Split Elapsed into new Task
                    if event.key() == QtCore.Qt.Key_S:
                        if not taskWidget.taskTextWidget.hasFocus():
                            taskWidget.showEditElapsed(split=True)
                    # Edit Task Text
                    if event.key() == QtCore.Qt.Key_T:
                        if not taskWidget.taskTextWidget.hasFocus():
                            taskWidget.taskTextWidget.setFocus()

                # Pause / Resume Task
                if event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                    if not taskWidget.taskTextWidget.hasFocus():
                        taskWidget.toggle()

                # Cancel Edit Elapsed
                if event.key() == QtCore.Qt.Key_Escape:
                    taskWidget.taskTextWidget.clearFocus()
                    taskWidget.editElapsedWidget.hide()
                    taskWidget.editElapsedButton.hide()
                    taskWidget.editElapsedCancelButton.hide()
                    taskWidget.timerWidget.show()

            self.updateButtonStatesSignal.emit()

        if propagate_event:
            super(self.__class__, self).keyPressEvent(event)

    def moveTasksUp(self):
        selected = self.selectedItems()
        if not selected:
            return

        for taskItem in sorted(selected, key=lambda x: self.row(x)):
            row = self.row(taskItem)
            new_row = row - 1
            if new_row < 0:
                new_row = self.count()

            taskWidget = self.itemWidget(taskItem)
            cloneItem = taskItem.clone()
            self.insertItem(new_row, cloneItem)
            self.setItemWidget(cloneItem, taskWidget)
            oldItem = self.takeItem(self.row(taskItem))
            cloneItem.setSelected(True)

    def moveTasksDown(self):
        selected = self.selectedItems()
        if not selected:
            return

        for taskItem in sorted(selected, key=lambda x: self.row(x), reverse=True):
            row = self.row(taskItem)
            new_row = row + 2
            if new_row > self.count():
                new_row = 0

            taskWidget = self.itemWidget(taskItem)
            cloneItem = taskItem.clone()
            self.insertItem(new_row, cloneItem)
            self.setItemWidget(cloneItem, taskWidget)
            oldItem = self.takeItem(self.row(taskItem))
            cloneItem.setSelected(True)

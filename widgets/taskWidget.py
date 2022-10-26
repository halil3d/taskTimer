#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import qtawesome
from qtpy import QtCore, QtGui, QtWidgets

from timerWidget import TimerWidget
from taskTextWidget import TaskTextWidgetDefault
from taskTimer import utils


class TaskWidget(QtWidgets.QWidget):
    addTaskSignal = QtCore.Signal(int)

    @classmethod
    def fromData(cls, data, taskTextWidget=None):
        taskWidget = cls(taskTextWidget=taskTextWidget)
        taskWidget.deserialise(data)
        return taskWidget

    def __init__(self, taskTextWidget=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._taskTextWidget = None
        self.taskTextWidget = taskTextWidget

        self.editElapsedWidget = QtWidgets.QLineEdit(self)

        escapeEvent = TaskWidgetEscapeEvent(self)
        self.editElapsedWidget.installEventFilter(escapeEvent)
        self.taskTextWidget.installEventFilter(escapeEvent)

        self.editElapsedWidget.setToolTip("Enter time as digits and units.")
        self.editElapsedButton = QtWidgets.QPushButton(
            qtawesome.icon("mdi.check", options=[{"color": "green"}]), ""
        )
        self.editElapsedButton.setToolTip("Confirm Time")
        self.editElapsedCancelButton = QtWidgets.QPushButton(
            qtawesome.icon("mdi.window-close", options=[{"color": "red"}]), ""
        )
        self.editElapsedCancelButton.setToolTip("Cancel")
        self.editElapsedCancelButton.hide()
        self.timerWidget = TimerWidget(self)
        bars = qtawesome.icon("mdi.drag")
        pixmap = bars.pixmap(24, 24)
        self.moveLabel = QtWidgets.QLabel()
        self.moveLabel.setPixmap(pixmap)
        # self.stopButton = QtWidgets.QPushButton("S")
        # self.resetButton = QtWidgets.QPushButton("R")

        self.setupUI()

    def setupUI(self):
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.editElapsedWidget.setFixedHeight(24)
        self.editElapsedWidget.setFixedWidth(80)
        self.editElapsedWidget.hide()
        self.editElapsedButton.hide()
        self.mainLayout.addWidget(self.editElapsedWidget)
        self.mainLayout.addWidget(self.editElapsedButton)
        self.mainLayout.addWidget(self.editElapsedCancelButton)
        self.mainLayout.addWidget(self.timerWidget)
        self.mainLayout.addWidget(self.taskTextWidget)
        self.mainLayout.addWidget(self.moveLabel)

        self.timerWidget.setToolTip("Double click to edit elapsed time (E)")
        # self.buttonLayout = QtWidgets.QHBoxLayout()
        # self.mainLayout.addLayout(self.buttonLayout)

        # self.stopButton.setFixedSize(24, 24)
        # self.resetButton.setFixedSize(24, 24)
        # self.buttonLayout.addWidget(self.stopButton)
        # self.buttonLayout.addWidget(self.resetButton)

        # self.stopButton.clicked.connect(self.stop)
        # self.resetButton.clicked.connect(self.reset)

        # self.taskTextWidget.setFocus()

        self.editElapsedWidget.textChanged.connect(self.editElapsedTextChanged)
        self.editElapsedButton.clicked.connect(self.editElapsed)
        self.editElapsedCancelButton.clicked.connect(self.editElapsedWidget.hide)
        self.editElapsedCancelButton.clicked.connect(self.editElapsedCancelButton.hide)
        self.editElapsedCancelButton.clicked.connect(self.timerWidget.show)

    @property
    def taskTextWidget(self):
        """
        If a custom taskTextWidget is not set, use the default.
        """
        return self._taskTextWidget

    @taskTextWidget.setter
    def taskTextWidget(self, taskTextWidget):
        if taskTextWidget is None:
            # No need to validate, default will be used
            taskTextWidget = TaskTextWidgetDefault
        elif not isinstance(taskTextWidget, TaskTextWidgetBase):
            raise TypeError("taskTextwidget must be a subclass of TaskTextWidgetBase")
        self._taskTextWidget = taskTextWidget(self)

    def serialise(self):
        data =  {
            "Task": self.taskTextWidget.serialise(),
            "Start": self.started().strftime(r"%Y-%m-%d %H:%M:%S"),
            "End": self.ended().strftime(r"%Y-%m-%d %H:%M:%S"),
            "Elapsed": utils.timeToString(
                self.elapsed(), inputUnit="ms", minUnit="s"
            )
        }
        return data

    def deserialise(self, data):
        self.taskTextWidget.deserialise(data['Task'])
        elapsed = utils.stringToTime(data['Elapsed'], "ms")
        self.setElapsed(elapsed)
        started = datetime.datetime.strptime(data['Start'], r"%Y-%m-%d %H:%M:%S")
        self.setStarted(started)
        ended = datetime.datetime.strptime(data['End'], r"%Y-%m-%d %H:%M:%S")
        self.setEnded(ended)
        self.stop()

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

    def setStarted(self, datetime):
        self.timerWidget.setStarted(datetime)

    def stop(self):
        self.timerWidget.stop()

    def ended(self):
        return self.timerWidget.ended()

    def setEnded(self, datetime):
        self.timerWidget.setEnded(datetime)

    def reset(self):
        self.timerWidget.reset()

    def toggle(self):
        self.timerWidget.toggle()

    def editElapsed(self):
        text = self.editElapsedWidget.text()
        text = text.strip()
        if text.startswith("split"):
            text = text.partition("split")[-1].strip(":").strip()
            if utils.isValidTimeString(text):
                split_elapsed = utils.stringToTime(text, "ms")
                if split_elapsed:
                    days, remainder = divmod(
                        split_elapsed, utils.timeMultiplier("days", "ms")
                    )
                    if not days:
                        current_elapsed = self.elapsed() - split_elapsed
                        if not current_elapsed >= 0:
                            self.hideEditElapsed()
                            self.timerWidget.show()
                            return

                        self.stop()
                        self.setElapsed(current_elapsed)
                        self.addTaskSignal.emit(split_elapsed)
            else:
                # Handled by editElapsedTextChanged
                pass
        else:
            if utils.isValidTimeString(text):
                elapsed = utils.stringToTime(text, "ms")
                days, remainder = divmod(
                    elapsed, utils.timeMultiplier("days", "ms")
                )
                if not days:
                    self.setElapsed(elapsed)
            else:
                pass
                # Handled by editElapsedTextChanged
                return

        self.hideEditElapsed()
        self.timerWidget.show()

    def editElapsedTextChanged(self, text):
        if text.startswith("split"):
            text = text.partition("split")[-1].strip(":")
        text = text.strip()

        if utils.isValidTimeString(text):
            self.editElapsedButton.setEnabled(True)
            self.editElapsedButton.show()
            self.editElapsedCancelButton.hide()
            self.editElapsedWidget.setStyleSheet(r"QLineEdit {background-color: #efffe3; border: 1px solid #91ff66}")
        else:
            self.editElapsedButton.hide()
            self.editElapsedCancelButton.show()
            self.editElapsedWidget.setStyleSheet(r"QLineEdit {background-color: #ffe4e4; border: 1px solid #f66}")

    def mouseDoubleClickEvent(self, event):
        if self.childAt(event.pos()) == self.timerWidget:
            self.showEditElapsed()

    def showEditElapsed(self, split=False):
        self.timerWidget.hide()

        if split:
            self.editElapsedWidget.setText("split: ")
        else:
            self.editElapsedWidget.setText("")

        self.editElapsedWidget.setStyleSheet("")
        self.editElapsedWidget.show()
        self.editElapsedWidget.setFocus()
        self.editElapsedCancelButton.setHidden(True)
        self.editElapsedButton.setEnabled(False)
        self.editElapsedButton.show()

    def hideEditElapsed(self):
        self.editElapsedWidget.setText("")
        self.editElapsedWidget.hide()
        self.editElapsedButton.hide()
        self.editElapsedCancelButton.hide()

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
            # Confirm Edit Elapsed Text
            if self.editElapsedWidget.hasFocus():
                self.editElapsedButton.click()
            # Confirm Task Text
            if self.taskTextWidget.hasFocus():
                self.taskTextWidget.clearFocus()
                self.parent().setFocus()
        super(self.__class__, self).keyPressEvent(event)


class TaskWidgetEscapeEvent(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                if obj.__class__ == QtWidgets.QLineEdit:
                    obj.hide()
                    obj.parent().taskTextWidget.clearFocus()
                    obj.parent().editElapsedButton.hide()
                    obj.parent().editElapsedCancelButton.hide()
                    obj.parent().timerWidget.show()
                else:
                    # class == taskTextWidget
                    obj.parent().parent().setFocus()
                return True
        return super(obj.__class__, obj).eventFilter(obj, event)

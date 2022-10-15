#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from qtpy import QtCore, QtGui, QtWidgets

from taskTimer import utils


class TimerWidget(QtWidgets.QLCDNumber):
    def __init__(self, *argss, **kwargs):
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
        self.setStyleSheet(
            "QLCDNumber{color: rgb(40, 180, 33); background-color: rgb(50, 70, 50);}"
        )

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

    def start(self):
        if not self.isActive():
            self._timerID = self.startTimer(1)
        if not self._started:
            self._started = datetime.datetime.now()
        self._timer.start()
        self.setStyleSheet(
            "QLCDNumber{color: rgb(40, 180, 33); background-color: rgb(50, 70, 50);}"
        )

    def started(self):
        # FIXME: Need to do something smart when timer has been created with set
        # time and was never activated, returning now() for now...
        return self._started or datetime.datetime.now()

    def setStarted(self, datetime):
        self._started = datetime

    def stop(self):
        if self._timerID:
            self._elapsed += self._timer.elapsed()
            self.killTimer(self._timerID)
            self._timerID = None
            self._ended = datetime.datetime.now()
        self.setStyleSheet(
            "QLCDNumber{color: rgb(100, 120, 92); background-color: rgb(50, 70, 50);}"
        )

    def ended(self):
        if self._timerID:
            self._ended = datetime.datetime.now()
        # FIXME: Need to do something smart when timer has been created with set
        # time and was never activated, returning now() for now...
        return self._ended or datetime.datetime.now()

    def setEnded(self, datetime):
        self._ended = datetime

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
        days, remainder = divmod(milliseconds, utils.timeMultiplier("days", "ms"))
        if days:
            raise Exception("Cannot set a value > 24 hours.")
        hours, remainder = divmod(remainder, utils.timeMultiplier("hours", "ms"))
        minutes, remainder = divmod(remainder, utils.timeMultiplier("mins", "ms"))
        seconds, remainder = divmod(remainder, utils.timeMultiplier("secs", "ms"))
        timestring = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
        self.display(timestring)

    def timerEvent(self, event):
        milliseconds = self._elapsed + self._timer.elapsed()
        self.displayMilliseconds(milliseconds)

#!/usr/bin/python
# -*- coding: utf-8
import datetime
from qtpy import QtWidgets

from taskTimer import timer
from taskTimer import utils


class TimerWidget(QtWidgets.QLCDNumber):
    def __init__(self, *argss, **kwargs):
        super(self.__class__, self).__init__(*argss, **kwargs)
        self._timerID = None
        self._timer = timer.Timer()
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
        return self._timer.isActive()

    def elapsed(self):
        return self._timer.elapsed()

    def setElapsed(self, value):
        self._timer.setElapsed(value)
        if self.isActive():
            self.start()
        else:
            self.displayDelta(value)

    def start(self):
        self._timer.start()
        self._timerID = self.startTimer(1)
        self.setStyleSheet(
            "QLCDNumber{color: rgb(40, 180, 33); background-color: rgb(50, 70, 50);}"
        )

    def started(self):
        return self._timer.started()

    def setStarted(self, value):
        self._timer.setStarted(value)

    def stop(self):
        self._timer.stop()
        if self._timerID:
            self.killTimer(self._timerID)
        self.setStyleSheet(
            "QLCDNumber{color: rgb(100, 120, 92); background-color: rgb(50, 70, 50);}"
        )

    def ended(self):
        return self._timer.ended()

    def setEnded(self, value):
        self._timer.setEnded(value)

    def reset(self):
        self.stop()
        self._timer.reset()
        self.display("00:00:00")

    def toggle(self):
        if self.isActive():
            self.stop()
        else:
            self.start()

    def displayDelta(self, value):
        days, remainder = divmod(value.total_seconds(), utils.timeMultiplier("days", "secs"))
        if days:
            raise Exception("Cannot set a value > 24 hours.")
        hours, remainder = divmod(remainder, utils.timeMultiplier("hours", "secs"))
        minutes, remainder = divmod(remainder, utils.timeMultiplier("mins", "secs"))
        seconds, remainder = divmod(remainder, utils.timeMultiplier("secs", "secs"))
        timestring = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
        self.display(timestring)

    def timerEvent(self, event):  #pylint: disable=unused-argument
        elapsed_delta = self.elapsed()
        self.displayDelta(elapsed_delta)

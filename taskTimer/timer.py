#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime


class Timer(object):
    def __init__(self):
        super(self.__class__, self).__init__()
        self._started = None
        self._elapsed_delta = datetime.timedelta(0)
        self._timer_start = None
        self._ended = None

    def isActive(self):
        if self._started and not self._ended:
            return True
        return False

    def start(self):
        # FIXME check orignal timerWidget logic
        self._ended = None
        if not self._started:
            self._started = datetime.datetime.now()
            self._timer_start = datetime.datetime.now()

    def elapsed(self):
        elapsed = None
        if self.isActive():
            elapsed = datetime.datetime.now() - self._timer_start + self._elapsed_delta
        else:
            elapsed = self.ended() - (self._timer_start or self._ended) + self._elapsed_delta
        return elapsed

    def setElapsed(self, value):
        if not isinstance(value, datetime.timedelta):
            raise ValueError(
                "Expected datetime.timedelta value, got: {}.".format(
                    type(value)))
        self._elapsed_delta = value
        if self.isActive():
            self._timer_start = datetime.datetime.now()
        else:
            self._timer_start = self._ended

    def started(self):
        # FIXME: Need to do something smart when timer has been created with set
        # time and was never activated, returning now() for now...
        return self._started or datetime.datetime.now()

    def setStarted(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError(
                "Expected datetime.datetime value, got: {}.".format(type(value)))
        self._started = value

    def stop(self):
        self._ended = datetime.datetime.now()

    def ended(self):
        if self.isActive():
            self._ended = datetime.datetime.now()
        # FIXME: Need to do something smart when timer has been created with set
        # time and was never activated, returning now() for now...
        self._ended = self._ended or datetime.datetime.now()
        return self._ended

    def setEnded(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError(
                "Expected datetime.datetime value, got: {}.".format(type(value)))
        self._ended = value

    def reset(self):
        self._started = None
        self._elapsed_delta = datetime.timedelta(0)
        self._timer_start = None
        self._ended = None

    def toggle(self):
        if self.isActive():
            self.stop()
        else:
            self.start()

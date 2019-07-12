from PySide import QtCore
from PySide import QtGui

# TODO: Buttons
# Stop active timer if any and start new
# cycle timer previous - Stop active timer if any and resume previous
# cycle timer next - Stop active timer if any and resume next

MILISECONDS_IN_AN_HOUR = 3600000
MILISECONDS_IN_A_MINUTE = 60000
MILISECONDS_IN_A_SECOND = 1000


class TaskTimer(QtGui.QWidget):
    def __init__(self, *arg, **kwarg):
        super(TaskTimer, self).__init__(*arg, **kwarg)
        self.setupUI()

    def setupUI(self):
        self.mainLayout = QtGui.QVBoxLayout()

        x, y, w, h = 100, 100, 350, 50
        self.setGeometry(x, y, w, h)

        self.lcdDisplay = TimerWidget(self)
        self.mainLayout.addWidget(self.lcdDisplay)
        self.setLayout(self.mainLayout)


class TimerWidget(QtGui.QWidget):
    def __init__(self, parent=None, displayButtons=True, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.displayButtons = displayButtons
        self.timerID = None
        self.elapsed = None

        self.timer = QtCore.QElapsedTimer()

        self.setupUI()
        self.resetTimer()

    def setupUI(self):
        self.mainlayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainlayout)

        self.lcdDisplay = QtGui.QLCDNumber(self)
        self.lcdDisplay.setDigitCount(8)
        self.mainlayout.addWidget(self.lcdDisplay)
        self.buttonLayout = QtGui.QHBoxLayout()

        if self.displayButtons:
            self.toggleButton = QtGui.QPushButton("S/S")
            self.resetButton = QtGui.QPushButton("R")
            self.buttonLayout.addWidget(self.toggleButton)
            self.buttonLayout.addWidget(self.resetButton)

            self.toggleButton.clicked.connect(self.toggleTimer)
            self.resetButton.clicked.connect(self.resetTimer)

        self.mainlayout.addLayout(self.buttonLayout)

    def startTimer(self):
        if not self.timerID:
            self.timerID = super(self.__class__, self).startTimer(1)
        self.timer.start()

    def stopTimer(self):
        if self.timerID:
            self.elapsed += self.timer.elapsed()
            self.killTimer(self.timerID)
            self.timerID = None

    def resetTimer(self):
        if self.timerID:
            self.killTimer(self.timerID)
            self.timerID = None

        self.elapsed = 0
        self.lcdDisplay.display("00:00:00")

    def toggleTimer(self):
        if self.timerID:
            self.stopTimer()
        else:
            self.startTimer()

    def timerEvent(self, event):
        milliseconds = self.elapsed + self.timer.elapsed()
        hours, remainder = divmod(milliseconds, MILISECONDS_IN_AN_HOUR)
        minutes, remainder = divmod(remainder, MILISECONDS_IN_A_MINUTE)
        seconds, milliseconds = divmod(remainder, MILISECONDS_IN_A_SECOND)
        delta = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
        self.lcdDisplay.display(delta)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimer()
    t.show()
    sys.exit(app.exec_())

from PySide import QtCore
from PySide import QtGui
# from . import utils
import utils

# TODO: Buttons
# Stop active timer if any and start new
# cycle timer previous - Stop active timer if any and resume previous
# cycle timer next - Stop active timer if any and resume next


class TaskTimer(QtGui.QWidget):

    def __init__(self, *arg, **kwarg):
        super(self.__class__, self).__init__(*arg, **kwarg)
        self.listWidget = QtGui.QListWidget(self)
        self.toggleNewTimer = QtGui.QPushButton("+")
        self.setupUI()

    def setupUI(self):
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        x, y, w, h = 100, 100, 350, 50
        self.setGeometry(x, y, w, h)

        self.mainLayout.addWidget(self.listWidget)
        self.mainLayout.addWidget(self.toggleNewTimer)

        self.toggleNewTimer.clicked.connect(self.addNewTask)

    def addNewTask(self):
        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            widget.stop()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(100, 50))
        newTask = TaskWidget()
        newTask.start()
        self.listWidget.setItemWidget(item, newTask)
        self.listWidget.addItem(item)


class TaskWidget(QtGui.QWidget):
    def __init__(self, *arg, **kwarg):
        super(self.__class__, self).__init__(*arg, **kwarg)
        self.taskLineEdit = QtGui.QLineEdit(self)
        self.timerWidget = TimerWidget(self)
        self.stopButton = QtGui.QPushButton("S")
        self.resetButton = QtGui.QPushButton("R")
        self.setupUI()

    def setupUI(self):
        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.taskLineEdit)
        self.mainLayout.addWidget(self.timerWidget)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.stopButton.setFixedSize(24, 24)
        self.resetButton.setFixedSize(24, 24)
        self.buttonLayout.addWidget(self.stopButton)
        self.buttonLayout.addWidget(self.resetButton)

        self.stopButton.clicked.connect(self.stop)
        self.resetButton.clicked.connect(self.reset)

    def start(self):
        self.timerWidget.start()

    def stop(self):
        self.timerWidget.stop()

    def reset(self):
        self.timerWidget.reset()

    def toggle(self):
        self.timerWidget.toggle()


class TimerWidget(QtGui.QLCDNumber):

    def __init__(self, parent=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.timerID = None
        self.elapsed = None
        self.timer = QtCore.QElapsedTimer()

        self.setDigitCount(8)
        self.setFixedHeight(24)
        self.setFixedWidth(120)

        self.reset()

    def start(self):
        if not self.timerID:
            self.timerID = self.startTimer(1)
        self.timer.start()

    def stop(self):
        if self.timerID:
            self.elapsed += self.timer.elapsed()
            self.killTimer(self.timerID)
            self.timerID = None

    def reset(self):
        if self.timerID:
            self.killTimer(self.timerID)
            self.timerID = None

        self.elapsed = 0
        self.display("00:00:00")

    def toggle(self):
        if self.timerID:
            self.stop()
        else:
            self.start()

    def timerEvent(self, event):
        milliseconds = self.elapsed + self.timer.elapsed()
        timestring = milli2LCDString(milliseconds)
        self.display(timestring)


def milli2LCDString(milliseconds):
    days = int(utils.convertTime(milliseconds, 'ms', 'days'))
    if days:
        raise Exception("Cannot set a value > 24 hours.")
    hours = int(utils.convertTime(milliseconds, 'ms', 'hours'))
    minutes = int(utils.convertTime(milliseconds, 'ms', 'mins'))
    seconds = int(utils.convertTime(milliseconds, 'ms', 'secs'))
    timestring = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
    return timestring


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv[1:])
    t = TaskTimer()
    t.show()
    sys.exit(app.exec_())

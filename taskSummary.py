#!/usr/bin/python
# -*- coding: utf-8 -*-

import qtawesome
from PySide import QtCore, QtGui

from taskTimer import utils


class TaskSummary(QtGui.QWidget):
    def __init__(self, taskWidgets=[], *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.taskWidgets = taskWidgets
        self._mousePressed = False
        self._mousePosition = None

        self.mainLayout = QtGui.QVBoxLayout(self)
        self.closeButton = QtGui.QPushButton(qtawesome.icon("mdi.window-close"), "")
        self.windowIconLayout = QtGui.QHBoxLayout()
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtGui.QTableView(self)

        self.setupUI()

    def setupUI(self):
        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
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

        sizeGrip = QtGui.QSizeGrip(self)
        self.mainLayout.addWidget(
            sizeGrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
        )

        headerRow = []
        for header in ["Task", "Start", "End", "Elapsed"]:
            headerRow.append(QtGui.QStandardItem(header))
        self.model.appendRow(headerRow)

        for taskWidget in self.taskWidgets:
            rowItems = [
                QtGui.QStandardItem(taskWidget.getTaskName()),
                QtGui.QStandardItem(taskWidget.started().strftime("%Y-%m-%d %H:%M:%S")),
                QtGui.QStandardItem(taskWidget.ended().strftime("%Y-%m-%d %H:%M:%S")),
                QtGui.QStandardItem(
                    utils.timeToString(
                        taskWidget.elapsed(), inputUnit="ms", minUnit="s"
                    )
                ),
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
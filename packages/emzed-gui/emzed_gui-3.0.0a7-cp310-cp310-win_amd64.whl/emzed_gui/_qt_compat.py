#!/usr/bin/env python

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets


class QSize(PyQt5.QtCore.QSize):
    def __init__(self, *args):
        if len(args) == 2:
            args = (int(args[0]), int(args[1]))
        super().__init__(*args)


class QPainter(PyQt5.QtGui.QPainter):
    def drawLine(self, *args):
        if isinstance(args[0], (int, float)):
            a, b, c, d = args
            return super().drawLine(int(a), int(b), int(c), int(d))
        return super().drawLine(*args)

    def fillRect(self, *args):
        if isinstance(args[0], (int, float)):
            a, b, c, d, brush = args
            return super().fillRect(int(a), int(b), int(c), int(d), brush)
        return super().fillRect(*args)

    def drawRect(self, *args):
        if isinstance(args[0], (int, float)):
            a, b, c, d = args
            return super().drawRect(int(a), int(b), int(c), int(d))
        return super().drawRect(*args)


class QRect(PyQt5.QtCore.QRect):
    def setLeft(self, x):
        super().setLeft(int(x))

    def setRight(self, x):
        super().setRight(int(x))

    def setTop(self, x):
        super().setTop(int(x))

    def setBottom(self, x):
        super().setBottom(int(x))

    def setWidth(self, w):
        super().setWidth(int(w))

    def setHeight(self, w):
        super().setHeight(int(w))

    def setRect(self, a, b, c, d):
        return super().setRect(int(a), int(b), int(c), int(d))

    def adjusted(self, a, b, c, d):
        return super().adjusted(int(a), int(b), int(c), int(d))


class QWidget(PyQt5.QtWidgets.QWidget):
    def contentsRect(self):
        return QRect(super().contentsRect())

    @staticmethod
    def setTabOrder(a, b, base=PyQt5.QtWidgets.QWidget):
        # get rid of warnings about noops:
        if a.parent() is not None and b.parent() is not None:
            base.setTabOrder(a, b)


class QSplitter(PyQt5.QtWidgets.QSplitter, QWidget):
    # inheritance decl fixes isintance checks
    pass


class QFrame(PyQt5.QtWidgets.QFrame):
    def contentsRect(self):
        return QRect(super().contentsRect())


def install():
    PyQt5.QtCore.QSize = QSize
    PyQt5.QtCore.QRect = QRect
    PyQt5.QtGui.QPainter = QPainter
    PyQt5.QtWidgets.QWidget = QWidget
    PyQt5.QtWidgets.QSplitter = QSplitter
    PyQt5.QtWidgets.QFrame = QFrame


    def qt_message_handler(mode, context, message):
        QtCore = PyQt5.QtCore
        if mode in (QtCore.QtInfoMsg, QtCore.QtWarningMsg):
            return
        elif mode == QtCore.QtCriticalMsg:
            mode = "CRITICAL"
        elif mode == QtCore.QtFatalMsg:
            mode = "FATAL"
        else:
            mode = "DEBUG"
        print("%s: %s\n" % (mode, message))


    PyQt5.QtCore.qInstallMessageHandler(qt_message_handler)

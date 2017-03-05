#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDial,
    QSpinBox,
    QLineEdit,
    QHBoxLayout,
)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)
        spinbox = QSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)

        dial.valueChanged[int].connect(spinbox.setValue)
        spinbox.valueChanged[int].connect(dial.setValue)

        # self.connect(dial, SIGNAL("valueChanged(int)"), spinbox.setValue)
        # self.connect(spinbox, SIGNAL("valueChanged(int)"), dial.setValue)
        self.setWindowTitle("Signals and Slots")


class Form2(QDialog):

    def __init__(self, parent=None):
        super(Form2, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)
        spinbox = QSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)

        dial.valueChanged[int].connect(spinbox.setValue)
        spinbox.valueChanged[int].connect(dial.setValue)
        # self.connect(dial, SIGNAL("valueChanged(int)"),
        #              spinbox, SLOT("setValue(int)"))
        # self.connect(spinbox, SIGNAL("valueChanged(int)"),
        #              dial, SLOT("setValue(int)"))
        self.setWindowTitle("Signals and Slots")


class ZeroSpinBox(QSpinBox):

    zeros = 0
    atzero = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ZeroSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.checkzero)
        # self.connect(self, SIGNAL("valueChanged(int)"), self.checkzero)

    def checkzero(self):
        if self.value() == 0:
            self.zeros += 1
            self.atzero.emit(self.zeros)
            # self.emit(SIGNAL("atzero"), self.zeros)


class Form3(QDialog):

    def __init__(self, parent=None):
        super(Form3, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)
        zerospinbox = ZeroSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(zerospinbox)
        self.setLayout(layout)

        dial.valueChanged[int].connect(zerospinbox.setValue)
        zerospinbox.valueChanged[int].connect(dial.setValue)
        # self.connect(dial, SIGNAL("valueChanged(int)"),
        #              zerospinbox, SLOT("setValue(int)"))
        # self.connect(zerospinbox, SIGNAL("valueChanged(int)"),
        #              dial, SLOT("setValue(int)"))
        zerospinbox.atzero.connect(self.announce)
        # self.connect(zerospinbox, SIGNAL("atzero"), self.announce)
        self.setWindowTitle("Signals and Slots")

    def announce(self, zeros):
        print("ZeroSpinBox has been at zero {} times".format(zeros))


class Form4(QDialog):

    def __init__(self, parent=None):
        super(Form4, self).__init__(parent)

        self.lineedit = QLineEdit()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.lineedit)
        self.setLayout(self.layout)

        self.lineedit.textChanged['QString'].connect(
            self.consoleEcho)
        # self.connect(lineedit, SIGNAL("textChanged(QString)"),
        #              self.consoleEcho)
        self.setWindowTitle("Signals and Slots")

    def consoleEcho(self, text):
        print(text)


class TaxRate(QObject):
    # rateChanged = pyqtSignal('double')

    def __init__(self):
        super(TaxRate, self).__init__()
        self.__rate = 17.5

    def rate(self):
        return self.__rate

    def setRate(self, rate):
        if rate != self.__rate:
            self.__rate = rate
            self.rateChanged.emit(self.__rate)
            # self.emit(SIGNAL("rateChanged"), self.__rate)


def rateChanged(value):
    print("TaxRate changed to {0:.2f}%".format(value))


app = QApplication(sys.argv)
form = None

if len(sys.argv) == 1 or sys.argv[1] == "1":
    form = Form()
elif sys.argv[1] == "2":
    form = Form2()
elif sys.argv[1] == "3":
    form = Form3()
elif sys.argv[1] == "4":
    form = Form4()

if form is not None:
    form.show()
    app.exec_()
else:  # if sys.argv[1] == "5"
    vat = TaxRate()
    vat.rateChanged.connect(rateChanged)
    # vat.connect(vat, SIGNAL("rateChanged"), rateChanged)
    vat.setRate(17.5)    # No change will occur (new rate is the same)
    vat.setRate(8.5)     # A change will occur (new rate is different)

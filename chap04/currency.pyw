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
import urllib.request

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)

        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)

        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)

        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)
        self.fromComboBox.currentIndexChanged[int].connect(
            self.updateUi)
        self.toComboBox.currentIndexChanged[int].connect(
            self.updateUi)
        self.fromSpinBox.valueChanged['double'].connect(
            self.updateUi)
        # self.connect(self.fromComboBox,
        #         SIGNAL("currentIndexChanged(int)"), self.updateUi)
        # self.connect(self.toComboBox,
        #         SIGNAL("currentIndexChanged(int)"), self.updateUi)
        # self.connect(self.fromSpinBox,
        #         SIGNAL("valueChanged(double)"), self.updateUi)
        self.setWindowTitle("Currency")

    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        ratio = (self.rates[from_] / self.rates[to])
        amount = ratio * self.fromSpinBox.value()
        self.toLabel.setText("{0:.2f}".format(amount))

    def getdata(self):  # Idea taken from the Python Cookbook
        self.rates = {}
        try:
            date = "Unknown"
            data = urllib.request.urlopen(
                "http://www.bankofcanada.ca"
                "/en/markets/csv/exchange_eng.csv").read()
            for line in data.decode("utf-8", "replace").split("\n"):
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing ")):
                    continue
                fields = line.split(",")
                if line.startswith("Date "):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0]] = value
                    except ValueError:
                        pass
            return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to download:\n{}".format(e)


app = QApplication(sys.argv)
form = Form()
form.show()

app.exec_()

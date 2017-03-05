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

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QGridLayout,
)


class NumberFormatDlg(QDialog):

    def __init__(self, format_, callback, parent=None):
        super(NumberFormatDlg, self).__init__(parent)
        punctuationRe = QRegExp(r"[ ,;:.]")

        self.thousandsEdit = QLineEdit(format_["thousandsseparator"])
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QRegExpValidator(
                punctuationRe, self))

        thousandsLabel = QLabel("&Thousands separator")
        thousandsLabel.setBuddy(self.thousandsEdit)

        self.decimalMarkerEdit = QLineEdit(format_["decimalmarker"])
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(QRegExpValidator(
                punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalMarkerLabel = QLabel("Decimal &marker")
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)

        self.decimalPlacesSpinBox = QSpinBox()
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format_["decimalplaces"])

        decimalPlacesLabel = QLabel("&Decimal places")
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)

        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format_["rednegatives"])

        self.format = format_
        self.callback = callback

        grid = QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        self.setLayout(grid)

        self.thousandsEdit.textEdited['QString'].connect(
            self.checkAndFix)
        self.decimalMarkerEdit.textEdited['QString'].connect(
            self.checkAndFix)
        self.decimalPlacesSpinBox.valueChanged[int].connect(
            self.apply)
        self.redNegativesCheckBox.toggled[bool].connect(
            self.apply)
        # self.connect(self.thousandsEdit,
        #         SIGNAL("textEdited(QString)"), self.checkAndFix)
        # self.connect(self.decimalMarkerEdit,
        #         SIGNAL("textEdited(QString)"), self.checkAndFix)
        # self.connect(self.decimalPlacesSpinBox,
        #         SIGNAL("valueChanged(int)"), self.apply)
        # self.connect(self.redNegativesCheckBox,
        #         SIGNAL("toggled(bool)"), self.apply)
        self.setWindowTitle("Set Number Format (`Live')")

    def checkAndFix(self):
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()

        if thousands == decimal:
            self.thousandsEdit.clear()
            self.thousandsEdit.setFocus()

        if len(decimal) == 0:
            self.decimalMarkerEdit.setText(".")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()

        self.apply()

    def apply(self):
        self.format["thousandsseparator"] = self.thousandsEdit.text()
        self.format["decimalmarker"] = self.decimalMarkerEdit.text()
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        self.callback()

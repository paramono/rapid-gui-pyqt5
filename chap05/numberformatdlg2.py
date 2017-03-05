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

from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QCheckBox,
    QSpinBox,
    QGridLayout,
)


class NumberFormatDlg(QDialog):

    changed = pyqtSignal()

    def __init__(self, format_, parent=None):
        super(NumberFormatDlg, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        punctuationRe = QRegExp(r"[ ,;:.]")

        self.thousandsEdit = QLineEdit(format_["thousandsseparator"])
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(
            QRegExpValidator(punctuationRe, self))

        thousandsLabel = QLabel("&Thousands separator")
        thousandsLabel.setBuddy(self.thousandsEdit)

        self.decimalPlacesSpinBox = QSpinBox()
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format_["decimalplaces"])

        self.decimalMarkerEdit = QLineEdit(format_["decimalmarker"])
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(
                QRegExpValidator(punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalMarkerLabel = QLabel("Decimal &marker")
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)

        decimalPlacesLabel = QLabel("&Decimal places")
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)

        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format_["rednegatives"])

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Close)

        self.format = format_

        grid = QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)

        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)

        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)

        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        grid.addWidget(buttonBox, 4, 0, 1, 2)
        self.setLayout(grid)

        buttonBox.button(QDialogButtonBox.Apply) \
            .clicked.connect(self.apply)
        buttonBox.rejected.connect(self.reject)
        # self.connect(buttonBox.button(QDialogButtonBox.Apply),
        #              SIGNAL("clicked()"), self.apply)
        # self.connect(buttonBox, SIGNAL("rejected()"),
        #              self, SLOT("reject()"))
        self.setWindowTitle("Set Number Format (Modeless)")

    def apply(self):
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
        if thousands == decimal:
            QMessageBox.warning(
                self,
                "Format Error",
                "The thousands separator and the decimal marker "
                "must be different.")
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QMessageBox.warning(
                self,
                "Format Error",
                "The decimal marker may not be empty.")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
            self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
            self.redNegativesCheckBox.isChecked())

        self.changed.emit()
        # self.emit(SIGNAL("changed"))

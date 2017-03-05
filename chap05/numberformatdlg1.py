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

    def __init__(self, format_, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        self.thousandsEdit = QLineEdit(format_["thousandsseparator"])
        thousandsLabel = QLabel("&Thousands separator")
        thousandsLabel.setBuddy(self.thousandsEdit)

        self.decimalMarkerEdit = QLineEdit(format_["decimalmarker"])

        decimalMarkerLabel = QLabel("Decimal &marker")
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)

        self.decimalPlacesSpinBox = QSpinBox()
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format_["decimalplaces"])

        decimalPlacesLabel = QLabel("&Decimal places")
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)

        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format_["rednegatives"])

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        self.format = format_.copy()

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

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        # self.connect(buttonBox, SIGNAL("accepted()"),
        #              self, SLOT("accept()"))
        # self.connect(buttonBox, SIGNAL("rejected()"),
        #              self, SLOT("reject()"))
        self.setWindowTitle("Set Number Format (Modal)")

    def accept(self):
        class ThousandsError(Exception):
            pass

        class DecimalError(Exception):
            pass

        Punctuation = frozenset(" ,;:.")
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()

        try:
            if len(decimal) == 0:
                raise DecimalError(
                    "The decimal marker may not be empty.")
            if len(thousands) > 1:
                raise ThousandsError(
                    "The thousands separator may "
                    "only be empty or one character.")
            if len(decimal) > 1:
                raise DecimalError(
                    "The decimal marker must be "
                    "one character.")
            if thousands == decimal:
                raise ThousandsError(
                    "The thousands separator and "
                    "the decimal marker must be different.")
            if thousands and thousands not in Punctuation:
                raise ThousandsError(
                    "The thousands separator must "
                    "be a punctuation symbol.")
            if decimal not in Punctuation:
                raise DecimalError(
                    "The decimal marker must be a "
                    "punctuation symbol.")
        except ThousandsError as e:
            QMessageBox.warning(self, "Thousands Separator Error", str(e))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        except DecimalError as e:
            QMessageBox.warning(self, "Decimal Marker Error", str(e))
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
            self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
            self.redNegativesCheckBox.isChecked())
        QDialog.accept(self)

    def numberFormat(self):
        return self.format

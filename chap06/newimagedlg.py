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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QPainter,
    QPixmap,
    QBrush,
)
from PyQt5.QtWidgets import (
    QDialog,
    QColorDialog,
    QApplication,
)

import ui_newimagedlg


class NewImageDlg(QDialog, ui_newimagedlg.Ui_NewImageDlg):

    def __init__(self, parent=None):
        super(NewImageDlg, self).__init__(parent)
        self.setupUi(self)

        self.color = Qt.red
        for value, text in (
            (Qt.SolidPattern, "Solid"),
            (Qt.Dense1Pattern, "Dense #1"),
            (Qt.Dense2Pattern, "Dense #2"),
            (Qt.Dense3Pattern, "Dense #3"),
            (Qt.Dense4Pattern, "Dense #4"),
            (Qt.Dense5Pattern, "Dense #5"),
            (Qt.Dense6Pattern, "Dense #6"),
            (Qt.Dense7Pattern, "Dense #7"),
            (Qt.HorPattern, "Horizontal"),
            (Qt.VerPattern, "Vertical"),
            (Qt.CrossPattern, "Cross"),
            (Qt.BDiagPattern, "Backward Diagonal"),
            (Qt.FDiagPattern, "Forward Diagonal"),
            (Qt.DiagCrossPattern, "Diagonal Cross")
        ):
            self.brushComboBox.addItem(text, value)

        self.colorButton.clicked.connect(self.getColor)
        self.brushComboBox.activated[int].connect(self.setColor)
        # self.connect(self.colorButton, SIGNAL("clicked()"),
        #              self.getColor)
        # self.connect(self.brushComboBox, SIGNAL("activated(int)"),
        #              self.setColor)
        self.setColor()
        self.widthSpinBox.setFocus()

    def getColor(self):
        color = QColorDialog.getColor(Qt.black, self)
        if color.isValid():
            self.color = color
            self.setColor()

    def setColor(self):
        pixmap = self._makePixmap(60, 30)
        self.colorLabel.setPixmap(pixmap)

    def image(self):
        pixmap = self._makePixmap(self.widthSpinBox.value(),
                                  self.heightSpinBox.value())
        return QPixmap.toImage(pixmap)

    def _makePixmap(self, width, height):
        pixmap = QPixmap(width, height)
        style = int(self.brushComboBox.itemData(
                    self.brushComboBox.currentIndex()))
        brush = QBrush(self.color, Qt.BrushStyle(style))
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), Qt.white)
        painter.fillRect(pixmap.rect(), brush)
        return pixmap


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = NewImageDlg()
    form.show()
    app.exec_()

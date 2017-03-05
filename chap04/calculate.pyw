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
from math import *

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QTextBrowser,
    QLineEdit,
    QVBoxLayout,
)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.line_edit = QLineEdit("Type an expression and press Enter")
        self.line_edit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        self.line_edit.setFocus()
        self.line_edit.returnPressed.connect(
            self.updateUi)
        # self.connect(
        #     self.line_edit,
        #     SIGNAL("returnPressed()"),
        #     self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.line_edit.text()
            self.browser.append("{} = <b>{}</b>".format(text,
                                eval(text)))
        except:
            self.browser.append("<font color=red>{} is invalid!</font>"
                                .format(text))


app = QApplication(sys.argv)
form = Form()
form.show()

app.exec_()

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

import functools
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QHBoxLayout,
    QPushButton
)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.button1 = QPushButton("One")
        self.button2 = QPushButton("Two")
        self.button3 = QPushButton("Three")
        self.button4 = QPushButton("Four")
        self.button5 = QPushButton("Five")
        self.label = QLabel("Click a button...")

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addStretch()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.button1.clicked.connect(self.one)
        # self.connect(button1, SIGNAL("clicked()"), self.one)

        self.button2callback = functools.partial(self.anyButton, "Two")
        self.button2.clicked.connect(self.button2callback)
        # self.connect(button2, SIGNAL("clicked()"),
        #              self.button2callback)

        self.button3callback = lambda _: self.anyButton('Three')
        self.button3.clicked.connect(self.button3callback)
        self.button4.clicked.connect(self.clicked)
        self.button5.clicked.connect(self.clicked)
        # self.connect(button3, SIGNAL("clicked()"),
        #              self.button3callback)
        # self.connect(button4, SIGNAL("clicked()"), self.clicked)
        # self.connect(button5, SIGNAL("clicked()"), self.clicked)

        self.setWindowTitle("Connections")

    def one(self):
        self.label.setText("You clicked button 'One'")

    def anyButton(self, who):
        self.label.setText("You clicked button '{}'".format(who))

    def clicked(self):
        button = self.sender()
        if button is None or not isinstance(button, QPushButton):
            return
        self.label.setText("You clicked button '{}'".format(
                           button.text()))


app = QApplication(sys.argv)
form = Form()
form.show()

app.exec_()

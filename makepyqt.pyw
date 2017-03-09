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

import os
import platform
import stat
import sys

from PyQt5.QtCore import (
    Qt,
    QSettings,
    QProcess,
    QDir,
    QFile,
    QT_VERSION_STR,
    PYQT_VERSION_STR,
)

from PyQt5.QtGui import QCursor

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QRadioButton,
    QDialogButtonBox,
    QCheckBox,
    QFrame,
    QDialog,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QTextBrowser,
    QTextEdit,
    QMenu,
)


__version__ = "5.0.0"


Windows = sys.platform.lower().startswith(("win", "microsoft"))


class OptionsForm(QDialog):

    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)

        settings = QSettings()
        if sys.platform.startswith("darwin"):
            pyuic5Label = QLabel("pyuic5 (pyuic.py)")
        else:
            pyuic5Label = QLabel("pyuic5")
        self.pyuic5Label = QLabel(settings.value("pyuic5", PYUIC5))
        self.pyuic5Label.setFrameStyle(QFrame.StyledPanel |
                                       QFrame.Sunken)
        pyuic5Button = QPushButton("py&uic5...")
        pyrcc5Label = QLabel("pyrcc5")
        self.pyrcc5Label = QLabel(settings.value("pyrcc5", PYRCC5))
        self.pyrcc5Label.setFrameStyle(QFrame.StyledPanel |
                                       QFrame.Sunken)
        pyrcc5Button = QPushButton("p&yrcc5...")
        pylupdate5Label = QLabel("pylupdate5")
        self.pylupdate5Label = QLabel(settings.value("pylupdate5",
                                      PYLUPDATE5))
        self.pylupdate5Label.setFrameStyle(QFrame.StyledPanel |
                                           QFrame.Sunken)
        pylupdate5Button = QPushButton("&pylupdate5...")
        lreleaseLabel = QLabel("lrelease")
        self.lreleaseLabel = QLabel(settings.value("lrelease", "lrelease"))
        self.lreleaseLabel.setFrameStyle(QFrame.StyledPanel |
                                         QFrame.Sunken)
        lreleaseButton = QPushButton("&lrelease...")
        toolPathGroupBox = QGroupBox("Tool Paths")

        pathsLayout = QGridLayout()
        pathsLayout.addWidget(pyuic5Label, 0, 0)
        pathsLayout.addWidget(self.pyuic5Label, 0, 1)
        pathsLayout.addWidget(pyuic5Button, 0, 2)
        pathsLayout.addWidget(pyrcc5Label, 1, 0)
        pathsLayout.addWidget(self.pyrcc5Label, 1, 1)
        pathsLayout.addWidget(pyrcc5Button, 1, 2)
        pathsLayout.addWidget(pylupdate5Label, 2, 0)
        pathsLayout.addWidget(self.pylupdate5Label, 2, 1)
        pathsLayout.addWidget(pylupdate5Button, 2, 2)
        pathsLayout.addWidget(lreleaseLabel, 3, 0)
        pathsLayout.addWidget(self.lreleaseLabel, 3, 1)
        pathsLayout.addWidget(lreleaseButton, 3, 2)
        toolPathGroupBox.setLayout(pathsLayout)

        resourceModuleNamesGroupBox = QGroupBox(
                "Resource Module Names")
        qrcFiles = bool(int(settings.value("qrc_resources", "1")))
        self.qrcRadioButton = QRadioButton("&qrc_file.py")
        self.qrcRadioButton.setChecked(qrcFiles)
        self.rcRadioButton = QRadioButton("file_&rc.py")
        self.rcRadioButton.setChecked(not qrcFiles)

        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.qrcRadioButton)
        radioLayout.addWidget(self.rcRadioButton)
        resourceModuleNamesGroupBox.setLayout(radioLayout)

        self.pyuic5xCheckBox = QCheckBox("Run pyuic5 with -&x "
                " to make forms stand-alone runable")
        x = bool(int(settings.value("pyuic5x", "0")))
        self.pyuic5xCheckBox.setChecked(x)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(toolPathGroupBox)
        layout.addWidget(resourceModuleNamesGroupBox)
        layout.addWidget(self.pyuic5xCheckBox)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        pyuic5Button.clicked.connect(lambda: self.setPath("pyuic5"))
        pyrcc5Button.clicked.connect(lambda: self.setPath("pyrcc5"))
        pylupdate5Button.clicked.connect(lambda: self.setPath("pylupdate5"))
        lreleaseButton.clicked.connect(lambda: self.setPath("lrelease"))

        # self.connect(pyuic5Button, SIGNAL("clicked()"),
        #         lambda: self.setPath("pyuic5"))
        # self.connect(pyrcc5Button, SIGNAL("clicked()"),
        #         lambda: self.setPath("pyrcc5"))
        # self.connect(pylupdate5Button, SIGNAL("clicked()"),
        #         lambda: self.setPath("pylupdate5"))
        # self.connect(lreleaseButton, SIGNAL("clicked()"),
        #         lambda: self.setPath("lrelease"))

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        # self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Make PyQt - Options")

    def accept(self):
        settings = QSettings()
        settings.setValue("pyuic5", self.pyuic5Label.text())
        settings.setValue("pyrcc5", self.pyrcc5Label.text())
        settings.setValue("pylupdate5", self.pylupdate5Label.text())
        settings.setValue("lrelease", self.lreleaseLabel.text())
        settings.setValue(
            "qrc_resources",
            "1" if self.qrcRadioButton.isChecked() else "0")
        settings.setValue(
            "pyuic5x",
            "1" if self.pyuic5xCheckBox.isChecked() else "0")
        QDialog.accept(self)

    def setPath(self, tool):
        if tool == "pyuic5":
            label = self.pyuic5Label
        elif tool == "pyrcc5":
            label = self.pyrcc5Label
        elif tool == "pylupdate5":
            label = self.pylupdate5Label
        elif tool == "lrelease":
            label = self.lreleaseLabel
        path = QFileDialog.getOpenFileName(
            self, "Make PyQt - Set Tool Path", label.text())
        if path:
            label.setText(QDir.toNativeSeparators(path))


class Form(QMainWindow):

    def __init__(self):
        super(Form, self).__init__(None)

        pathLabel = QLabel("Path:")
        settings = QSettings()
        rememberPath = None
        try:
            rememberPath = bool(int(
                settings.value("rememberpath", 1 if Windows else 0)))
        except ValueError:
            rememberPath = True if rememberPath == "true" else False
        if rememberPath:
            path = settings.value("path") or os.getcwd()
        else:
            path = (sys.argv[1] if len(sys.argv) > 1 and
                    QFile.exists(sys.argv[1]) else os.getcwd())
        self.pathLabel = QLabel(path)
        self.pathLabel.setFrameStyle(QFrame.StyledPanel |
                                     QFrame.Sunken)
        self.pathLabel.setToolTip(
            "The relative path; all actions will "
            "take place here,<br>and in this path's subdirectories "
            "if the Recurse checkbox is checked")
        self.pathButton = QPushButton("&Path...")
        self.pathButton.setToolTip(self.pathLabel.toolTip().replace(
            "The", "Sets the"))
        self.recurseCheckBox = QCheckBox("&Recurse")
        self.recurseCheckBox.setToolTip(
            "Clean or build all the files "
            "in the path directory,<br>and all its subdirectories, "
            "as deep as they go.")
        self.transCheckBox = QCheckBox("&Translate")
        self.transCheckBox.setToolTip(
            "Runs <b>pylupdate5</b> on all "
            "<tt>.py</tt> and <tt>.pyw</tt> files in conjunction "
            "with each <tt>.ts</tt> file.<br>Then runs "
            "<b>lrelease</b> on all <tt>.ts</tt> files to produce "
            "corresponding <tt>.qm</tt> files.<br>The "
            "<tt>.ts</tt> files must have been created initially by "
            "running <b>pylupdate5</b><br>directly on a <tt>.py</tt> "
            "or <tt>.pyw</tt> file using the <tt>-ts</tt> option.")
        self.debugCheckBox = QCheckBox("&Dry Run")
        self.debugCheckBox.setToolTip(
            "Shows the actions that would "
            "take place but does not do them.")
        self.logBrowser = QTextBrowser()
        self.logBrowser.setLineWrapMode(QTextEdit.NoWrap)
        self.buttonBox = QDialogButtonBox()
        menu = QMenu(self)
        optionsAction = menu.addAction("&Options...")
        self.rememberPathAction = menu.addAction("&Remember path")
        self.rememberPathAction.setCheckable(True)
        self.rememberPathAction.setChecked(rememberPath)
        aboutAction = menu.addAction("&About")
        moreButton = self.buttonBox.addButton(
            "&More", QDialogButtonBox.ActionRole)
        moreButton.setMenu(menu)
        moreButton.setToolTip(
            "Use <b>More-&gt;Tool paths</b> to set the "
            "paths to the tools if they are not found by default")
        self.buildButton = self.buttonBox.addButton(
            "&Build",
            QDialogButtonBox.ActionRole)
        self.buildButton.setToolTip(
            "Runs <b>pyuic5</b> on all "
            "<tt>.ui</tt> "
            "files and <b>pyrcc5</b> on all <tt>.qrc</tt> files "
            "that are out-of-date.<br>Also runs <b>pylupdate5</b> "
            "and <b>lrelease</b> if the Translate checkbox is "
            "checked.")
        self.cleanButton = self.buttonBox.addButton(
            "&Clean",
            QDialogButtonBox.ActionRole)
        self.cleanButton.setToolTip(
            "Deletes all <tt>.py</tt> files that "
            "were generated from <tt>.ui</tt> and <tt>.qrc</tt> "
            "files,<br>i.e., all files matching <tt>qrc_*.py</tt>, "
            "<tt>*_rc.py</tt> and <tt>ui_*.py.")
        quitButton = self.buttonBox.addButton(
            "&Quit",
            QDialogButtonBox.RejectRole)

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)
        topLayout.addWidget(self.pathButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.recurseCheckBox)
        bottomLayout.addWidget(self.transCheckBox)
        bottomLayout.addWidget(self.debugCheckBox)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.logBrowser)
        layout.addLayout(bottomLayout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        aboutAction.triggered.connect(self.about)
        optionsAction.triggered.connect(self.setOptions)
        self.pathButton.clicked.connect(self.setPath)
        self.buildButton.clicked.connect(self.build)
        self.cleanButton.clicked.connect(self.clean)
        quitButton.clicked.connect(self.close)

        # self.connect(aboutAction, SIGNAL("triggered()"), self.about)
        # self.connect(optionsAction, SIGNAL("triggered()"), self.setOptions)
        # self.connect(self.pathButton, SIGNAL("clicked()"), self.setPath)
        # self.connect(self.buildButton, SIGNAL("clicked()"), self.build)
        # self.connect(self.cleanButton, SIGNAL("clicked()"), self.clean)
        # self.connect(quitButton, SIGNAL("clicked()"), self.close)

        self.setWindowTitle("Make PyQt")

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue(
            "rememberpath",
            1 if self.rememberPathAction.isChecked() else 0)
        settings.setValue("path", self.pathLabel.text())
        event.accept()

    def about(self):
        QMessageBox.about(
            self,
            "About Make PyQt",
            """<b>Make PyQt</b> v {0}
            <p>Copyright &copy; 2007-10 Qtrac Ltd.
            All rights reserved.
            <p>This application can be used to build PyQt
            applications.
            It runs pyuic5, pyrcc5, pylupdate5, and lrelease as
            required, although pylupdate5 must be run directly to
            create the initial .ts files.
            <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__,
                platform.python_version(),
                QT_VERSION_STR,
                PYQT_VERSION_STR,
                platform.system()
            )
        )

    def setPath(self):
        path = QFileDialog.getExistingDirectory(
            self, "Make PyQt - Set Path", self.pathLabel.text())
        if path:
            self.pathLabel.setText(QDir.toNativeSeparators(path))

    def setOptions(self):
        dlg = OptionsForm(self)
        dlg.exec_()

    def build(self):
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = self.pathLabel.text()
        self._apply(recurse, self._build, path)
        if self.transCheckBox.isChecked():
            self._apply(recurse, self._translate, path)
        self.updateUi(True)

    def clean(self):
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = self.pathLabel.text()
        self._apply(recurse, self._clean, path)
        self.updateUi(True)

    def updateUi(self, enable):
        for widget in (
            self.buildButton,
            self.cleanButton,
            self.pathButton,
            self.recurseCheckBox,
            self.transCheckBox,
            self.debugCheckBox
        ):
            widget.setEnabled(enable)
        if not enable:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        else:
            QApplication.restoreOverrideCursor()
            self.buildButton.setFocus()

    def _apply(self, recurse, function, path):
        if not recurse:
            function(path)
        else:
            for root, dirs, files in os.walk(path):
                for dir in sorted(dirs):
                    function(os.path.join(root, dir))

    def _make_error_message(self, command, process):
        err = ""
        ba = process.readAllStandardError()
        if not ba.isEmpty():
            err = ": " + str(ba)
        return "<font color=red>FAILED: %s%s</font>" % (command, err)

    def _build(self, path):
        settings = QSettings()
        pyuic5 = settings.value("pyuic5", PYUIC5)
        pyrcc5 = settings.value("pyrcc5", PYRCC5)
        prefix = self.pathLabel.text()
        prefix = self.pathLabel.text()
        pyuic5x = bool(int(settings.value("pyuic5x", "0")))
        if not prefix.endswith(os.sep):
            prefix += os.sep
        failed = 0
        process = QProcess()
        for name in os.listdir(path):
            source = os.path.join(path, name)
            target = None
            if source.endswith(".ui"):
                target = os.path.join(path,
                                    "ui_" + name.replace(".ui", ".py"))
                command = pyuic5
            elif source.endswith(".qrc"):
                if bool(int(settings.value("qrc_resources", "1"))):
                    target = os.path.join(path,
                            "qrc_" + name.replace(".qrc", ".py"))
                else:
                    target = os.path.join(path, name.replace(".qrc", "_rc.py"))
                command = pyrcc5
            if target is not None:
                if not os.access(target, os.F_OK) or (
                   os.stat(source)[stat.ST_MTIME] >
                   os.stat(target)[stat.ST_MTIME]):
                    args = ["-o", target, source]
                    if command == pyrcc5:
                        args.insert(0, "-py3")
                    elif command == PYUIC5 and pyuic5x:
                        args.insert(0, "-x")
                    if (sys.platform.startswith("darwin") and
                        command == PYUIC5):
                        command = sys.executable
                        args = [PYUIC5] + args
                    msg = ("converted <font color=darkblue>" + source +
                           "</font> to <font color=blue>" + target +
                           "</font>")
                    if self.debugCheckBox.isChecked():
                        msg = "<font color=green># " + msg + "</font>"
                    else:
                        process.start(command, args)
                        if (not process.waitForFinished(2 * 60 * 1000) or
                            not QFile.exists(target)):
                            msg = self._make_error_message(command,
                                                           process)
                            failed += 1
                    self.logBrowser.append(msg.replace(prefix, ""))
                else:
                    self.logBrowser.append("<font color=green>"
                            "# {} is up-to-date</font>".format(
                            source.replace(prefix, "")))
                QApplication.processEvents()
        if failed:
            QMessageBox.information(self, "Make PyQt - Failures",
                    "Try manually setting the paths to the tools "
                    "using <b>More-&gt;Options</b>")


    def _clean(self, path):
        prefix = self.pathLabel.text()
        if not prefix.endswith(os.sep):
            prefix += os.sep
        deletelist = []
        for name in os.listdir(path):
            target = os.path.join(path, name)
            source = None
            if (target.endswith(".py") or target.endswith(".pyc") or
                target.endswith(".pyo")):
                if name.startswith("ui_") and not name[-1] in "oc":
                    source = os.path.join(path, name[3:-3] + ".ui")
                elif name.startswith("qrc_"):
                    if target[-1] in "oc":
                        source = os.path.join(path, name[4:-4] + ".qrc")
                    else:
                        source = os.path.join(path, name[4:-3] + ".qrc")
                elif name.endswith(("_rc.py", "_rc.pyo", "_rc.pyc")):
                    if target[-1] in "oc":
                        source = os.path.join(path, name[:-7] + ".qrc")
                    else:
                        source = os.path.join(path, name[:-6] + ".qrc")
                elif target[-1] in "oc":
                    source = target[:-1]
                if source is not None:
                    if os.access(source, os.F_OK):
                        if self.debugCheckBox.isChecked():
                            self.logBrowser.append("<font color=green>"
                                    "# delete {}</font>".format(
                                    target.replace(prefix, "")))
                        else:
                            deletelist.append(target)
                    else:
                        self.logBrowser.append("<font color=darkred>"
                                "will not remove "
                                "'{}' since `{}' not found</font>"
                                .format(target.replace(prefix, ""),
                                source.replace(prefix, "")))
        if not self.debugCheckBox.isChecked():
            for target in deletelist:
                self.logBrowser.append("deleted "
                        "<font color=red>{}</font>".format(
                        target.replace(prefix, "")))
                os.remove(target)
                QApplication.processEvents()


    def _translate(self, path):
        prefix = self.pathLabel.text()
        if not prefix.endswith(os.sep):
            prefix += os.sep
        files = []
        tsfiles = []
        for name in os.listdir(path):
            if name.endswith((".py", ".pyw")):
                files.append(os.path.join(path, name))
            elif name.endswith(".ts"):
                tsfiles.append(os.path.join(path, name))
        if not tsfiles:
            return
        settings = QSettings()
        pylupdate5 = settings.value("pylupdate5", PYLUPDATE5)
        lrelease = settings.value("lrelease", LRELEASE)
        process = QProcess()
        failed = 0
        for ts in tsfiles:
            qm = ts[:-3] + ".qm"
            command1 = pylupdate5
            args1 = files + ["-ts", ts]
            command2 = lrelease
            args2 = ["-silent", ts, "-qm", qm]
            msg = "updated <font color=blue>{}</font>".format(
                    ts.replace(prefix, ""))
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># {}</font>".format(msg)
            else:
                process.start(command1, args1)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = self._make_error_message(command1, process)
                    failed += 1
            self.logBrowser.append(msg)
            msg = "generated <font color=blue>{}</font>".format(
                    qm.replace(prefix, ""))
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># {}</font>".format(msg)
            else:
                process.start(command2, args2)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = self._make_error_message(command2, process)
                    failed += 1
            self.logBrowser.append(msg)
            QApplication.processEvents()
        if failed:
            QMessageBox.information(
                self,
                "Make PyQt - Failures",
                "Try manually setting the paths to the tools "
                "using <b>More-&gt;Options</b>"
            )


app = QApplication(sys.argv)
PATH = app.applicationDirPath()
if Windows:
    PATH = os.path.join(os.path.dirname(sys.executable),
                        "Lib/site-packages/PyQt5")
    if os.access(os.path.join(PATH, "bin"), os.R_OK):
        PATH = os.path.join(PATH, "bin")
if sys.platform.startswith("darwin"):
    i = PATH.find("Resources")
    if i > -1:
        PATH = PATH[:i] + "bin"
PYUIC5 = os.path.join(PATH, "pyuic5")
if sys.platform.startswith("darwin"):
    PYUIC5 = os.path.dirname(sys.executable)
    i = PYUIC5.find("Resources")
    if i > -1:
        PYUIC5 = PYUIC5[:i] + "Lib/python2.6/site-packages/PyQt5/uic/pyuic.py"
PYRCC5 = os.path.join(PATH, "pyrcc5")
PYLUPDATE5 = os.path.join(PATH, "pylupdate5")
LRELEASE = "lrelease"
if Windows:
    PYUIC5 = PYUIC5.replace("/", "\\") + ".bat"
    PYRCC5 = PYRCC5.replace("/", "\\") + ".exe"
    PYLUPDATE5 = PYLUPDATE5.replace("/", "\\") + ".exe"
app.setOrganizationName("Qtrac Ltd.")
app.setOrganizationDomain("qtrac.eu")
app.setApplicationName("Make PyQt")
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    settings = QSettings()
    settings.setValue("pyuic5", PYUIC5)
    settings.setValue("pyrcc5", PYRCC5)
    settings.setValue("pylupdate5", PYLUPDATE5)
    settings.setValue("lrelease", LRELEASE)
form = Form()
form.show()
app.exec_()

# 1.0.1 Fixed bug reported by Brian Downing where paths that contained
#       spaces were not handled correctly.
# 1.0.2 Fixed bug reported by Ben Thompson that if the UIC program
#       fails, no problem was reported; I try to report one now.
# 1.1.0 Added Remember path option; if checked the program starts with
#       the last used path, otherwise with the current directory, unless
#       overridden on the command line
# 1.1.1 Changed default path on Windows to match PyQt 4.4
# 1.2.1 Changed import style + bug fixes
# 1.2.2 Added stderr to error message output as per Michael Jackson's
#       suggestion
# 1.2.3 Tried to make the paths work on Mac OS X
# 1.3.0 Updated to Python 3.1
# 1.3.1 Added more options
# 1.3.2 Updates for Windows 7 and newer PyQts

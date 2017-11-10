# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstgui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_myfirstgui(object):
    def setupUi(self, myfirstgui):
        myfirstgui.setObjectName(_fromUtf8("myfirstgui"))
        myfirstgui.resize(411, 247)
        self.buttonBox = QtGui.QDialogButtonBox(myfirstgui)
        self.buttonBox.setGeometry(QtCore.QRect(20, 210, 381, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.myTextInput = QtGui.QLineEdit(myfirstgui)
        self.myTextInput.setGeometry(QtCore.QRect(10, 10, 101, 21))
        self.myTextInput.setObjectName(_fromUtf8("myTextInput"))
        self.listWidget = QtGui.QListWidget(myfirstgui)
        self.listWidget.setGeometry(QtCore.QRect(120, 10, 281, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.clearBtn = QtGui.QPushButton(myfirstgui)
        self.clearBtn.setGeometry(QtCore.QRect(10, 180, 101, 23))
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.addBtn = QtGui.QPushButton(myfirstgui)
        self.addBtn.setGeometry(QtCore.QRect(10, 40, 101, 23))
        self.addBtn.setObjectName(_fromUtf8("addBtn"))

        self.retranslateUi(myfirstgui)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), myfirstgui.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), myfirstgui.reject)
        QtCore.QObject.connect(self.clearBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.listWidget.clear)
        QtCore.QMetaObject.connectSlotsByName(myfirstgui)

    def retranslateUi(self, myfirstgui):
        myfirstgui.setWindowTitle(_translate("myfirstgui", "My First Gui!", None))
        self.clearBtn.setText(_translate("myfirstgui", "clear", None))
        self.addBtn.setText(_translate("myfirstgui", "add", None))


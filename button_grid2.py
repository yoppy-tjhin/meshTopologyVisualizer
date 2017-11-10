# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'button_grid.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 298)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(9, 262, 176, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 41, 51))
        self.label.setAutoFillBackground(False)

        bulbPixmap = QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg")
        #bulbPixmap.fill(QtCore.Qt.transparent)
        #bulbPixmap.fill(QtGui.QColor(255,0,0, 100))

        p = QPainter()
        p.begin(bulbPixmap)
        # p.setOpacity(0.5)
        #
        # p.drawPixmap(0, 0, bulbPixmap)

        #p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        #bg = QtGui.QColor(QtWidgets.QWidget.palette(self).color(QtGui.QPalette.Background))
        # opac = QtWidgets.QGraphicsOpacityEffect()
        # opac.setOpacity(1)
        # self.setGraphicsEffect(opac)
        #opac.draw(p)

        p.fillRect(bulbPixmap.rect(), QtGui.QColor(174, 167, 159 ,250))
        #p.fillRect(bulbPixmap.rect(), QtGui.QColor(69, 69, 69, 250))
        p.end()



        # QLabel * l = new
        # QLabel(this);
        # QImage
        # image(":/img/myimage.png");
        # QPainter
        # p;
        # p.begin( & image);
        # p.setCompositionMode(QPainter::CompositionMode_DestinationIn);
        # p.fillRect(image.rect(), QColor(0, 0, 0, 50));
        # p.end();
        # l->setPixmap(QPixmap::fromImage(image));


        self.label.setText("")
        self.label.setPixmap(bulbPixmap)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        #self.label.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 41, 51))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))

        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(160, 30, 41, 51))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(220, 30, 41, 51))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(220, 100, 41, 51))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(160, 100, 41, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(100, 100, 41, 51))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(50, 100, 41, 51))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("../../Documents/insinas 2017/python/bulb.jpeg"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(110, 180, 171, 17))
        self.label_9.setStyleSheet("background-color: rgb(255, 102, 135);")
        self.label_9.setObjectName("label_9")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_9.setText(_translate("Dialog", "adasfsafasf"))


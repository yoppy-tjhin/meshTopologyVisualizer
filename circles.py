# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'circles.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from read_serial import Serial
from node_mapping import NodeMapping
import threading, time, re

class Ui_MainWindow(object):
    #changedValue = pyqtSignal(int)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.mainX = 600
        self.mainY = 600
        self.nodeDiam = 50
        self.nodeRadius = self.nodeDiam/2
        self.nodeSpacing = 60
        MainWindow.resize(self.mainX, self.mainY)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.totalNodes = 3
        self.currentNumOfNodes = self.totalNodes
        self.drawNodes(self.currentNumOfNodes)
        # for k in range(6):
        #     self.label = QtWidgets.QLabel(self.centralwidget)
        #     self.label.setGeometry(QtCore.QRect(30+(80*k), 30, 60, 60))
        #     self.label.setObjectName("label")
        #
        #     pixmap = QtGui.QPixmap(71, 71)
        #     pixmap.fill(QtGui.QColor("white"))
        #
        #     painter = QtGui.QPainter()
        #     painter.begin(pixmap)
        #     painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0 ,(20+50*k))))
        #     painter.drawEllipse(0, 0, 70, 70)
        #     #painter.fillRect(pixmap.rect(), QtGui.QColor(174, 167, 159 ,255))
        #     painter.end()
        #     self.label.setPixmap(pixmap)
        #     self.label.setScaledContents(True)
        #     self.label_list.append(self.label)

        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(30, 30, 60, 60))
        # self.label.setObjectName("label")
        #
        # pixmap = QtGui.QPixmap(71, 71)
        # pixmap.fill(QtGui.QColor("white"))
        #
        # painter = QtGui.QPainter()
        # painter.begin(pixmap)
        # painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0 ,20)))
        # painter.drawEllipse(0, 0, 70, 70)
        # #painter.fillRect(pixmap.rect(), QtGui.QColor(174, 167, 159 ,255))
        # painter.end()
        # self.label.setPixmap(pixmap)
        # self.label.setScaledContents(True)
        #
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setGeometry(QtCore.QRect(140, 70, 31, 31))
        # self.label_2.setObjectName("label_2")

        # Create LineEdit

        #define lineEdit
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 230, 60, 20))
        self.lineEdit.setMaxLength(2)
        self.lineEdit.setAlignment(Qt.AlignLeft)
        #self.lineEdit.setFont(QFont("Arial", 20))
        self.lineEdit.setValidator(QIntValidator())
        # Setting a connection between slider position change and on_changed_value function
        self.lineEdit.returnPressed.connect(self.redrawNodes)


        # declare QPainter for drawing lines
        #self.painter = QPainter(self.centralwidget)
        self.painter = QPainter()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def drawLine(self, event, qp):

        qp.setPen(QColor(200, 0, 0))
        #qp.drawLine(300,300,50*self.currentNumOfNodes,100)
        x1 = self.mainX/2 + self.nodeRadius
        y1 = self.mainY/2
        x2 = self.mainX/2 + self.nodeSpacing - self.nodeRadius
        y2 = self.mainY/2
        #print (x1, y1, x2, y2)
        qp.drawLine(x1, y1, 600, y2)
        self.update()
        #print ("in drawLIne")

    def paintEvent(self, event):
        #rect = QRect(event.rect())
        #print (rect)
        #self.painter.eraseRect(QRect( 0, 0,  300, 300 ))
        self.painter.begin(self)
        self.drawLine(event, self.painter)
        self.painter.end()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "TextLabel"))
        #self.label_2.setText(_translate("MainWindow", "TextLabel"))

    def drawNodes(self, numOfNodes):
        self.label_list = []
        for k in range(numOfNodes):
            self.label = QtWidgets.QLabel(self.centralwidget)
            #self.label.setGeometry(QtCore.QRect(30+(80*k), 30, 60, 60))
            #self.label.setGeometry(QtCore.QRect(self.mainX/2 + (80 * k), self.mainY/2, self.nodeRadius*2, self.nodeRadius*2))

            x = self.mainX/2 - self.nodeRadius +  (self.nodeSpacing * k)
            y = self.mainY/2 - self.nodeRadius
            width = self.nodeDiam + 1   # offset needed to fully contain the circle
            height = self.nodeDiam + 1  # offset needed to fully contain the circle
            #print (x,y,width,height)
            self.label.setGeometry(QtCore.QRect(x, y, width, height))
            self.label.setObjectName("label" + str(k))

            pixmap = QtGui.QPixmap(width, height)
            #pixmap.fill(QtGui.QColor("gray"))
            pixmap.fill(self.centralwidget.palette().color(QPalette.Background))

            painter = QtGui.QPainter()
            painter.begin(pixmap)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0 ,255)))
            painter.drawEllipse(0, 0, self.nodeDiam, self.nodeDiam)
            #painter.fillRect(pixmap.rect(), QtGui.QColor(174, 167, 159 ,255))
            painter.end()
            self.label.setPixmap(pixmap)
            #self.label.setScaledContents(True)
            self.label_list.append(self.label)

    def redrawNodes(self):
        #self.drawNodes( int(self.text) )

        # for k in range(self.totalNodes):
        #     self.label_list[k].hide()

        #self.label_list[int(self.text)].hide()
        for k in range (self.currentNumOfNodes):
            self.label_list[k].deleteLater()

        # getting number from LineEdit
        self.currentNumOfNodes = int(self.lineEdit.text())
        self.drawNodes(self.currentNumOfNodes)

        for k in range(self.currentNumOfNodes):
            self.label_list[k].show()

    # Running task
    def node_visualizer_task(self, serialPort):

        nodeMapping = NodeMapping()
        # relation_list = nodeMapping.recursive_node_mapping()
        # self.drawLine(relation_list)
        # self.drawNodes(relation_list)

        # UNCOMMENT 'while' for use in threading mode
        while True:
            #lock = threading.Lock()
            #lock.acquire()
            jsonString = serialPort.read_json_string()  # read a '\n' terminated line
            if jsonString != None:  print (jsonString)
            #nodeMapping.recursive_node_mapping(jsonString)
            # print (line)
            # lock.release()
            # print (line)
            # if line:  # check if the serial bytes is not empty
            #     line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))  # only take JSON strings
            #     if (line_json != None):
            #         # lock.acquire()
            #         print( line_json.group(1) )
            #         # lock.release()
            # time.sleep(0.5)         # when it is not a JSON string
            # else:
            #     return None
            # if (line_json != None):
            #     lock.acquire()
            #     print( line_json.group(1) )
            #     lock.release()
            time.sleep(0.5)

    def run_node_visualizer_thread(self, serialPort):
        # serial_port = serial.Serial(self.comPort, self.baudRate, timeout=0)
        # thread = threading.Thread(target=self.read_from_port, args=(serial_port,))     # example, with args
        thread = threading.Thread(target=self.node_visualizer_task, args=( serialPort,))
        thread.start()


    # """
    # Initializing serial port.
    # :return: serialObj
    # """
    # def init_serial(self, comPort=None, baudRate=115200):
    #     serialObj = Serial(comPort, baudRate)
    #     return serialObj
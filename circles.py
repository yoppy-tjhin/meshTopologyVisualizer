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
from node_mapping import recursive_node_mapping
import time, re, json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

class Ui_MainWindow(object):
    #changedValue = pyqtSignal(int)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ESP8266 Mesh Network Topology Visualizer")
        self.mainX = 600
        self.mainY = 600
        MainWindow.resize(self.mainX, self.mainY)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        # a figure instance to plot on
        # self.figure = plt.figure()
        self.figure, self.node_collection = self.setupPlot()  # yoppy
        self.i = 1
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.draw()

        # register button pressed event
        self.cid = self.canvas.mpl_connect('button_press_event', self.onclick)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        updateMesh = GetMeshFromSerialThread()
        updateMesh.updateNode.connect(self.redrawMesh)
        updateMesh.start()

        #define lineEdit
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 230, 60, 20))
        self.lineEdit.setMaxLength(2)
        self.lineEdit.setAlignment(Qt.AlignLeft)
        #self.lineEdit.setFont(QFont("Arial", 20))
        self.lineEdit.setValidator(QIntValidator())
        # Setting a connection between slider position change and on_changed_value function
        self.lineEdit.returnPressed.connect(self.redrawMesh)

        #define label for serial setting
        self.serialSettingLabel = QLabel(self.centralwidget)
        self.serialSettingLabel.setText(updateMesh.getSerialSetting())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.serialSettingLabel)
        self.centralwidget.setLayout(layout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # on clicking UI
    def onclick(self,event):
        cont, ind = self.node_collection.contains(event)
        if cont:
            # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #       ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))

            #print ('ind: ')
            #print( self.G[ind['ind'][0]] )
            #print(self.G[1])
            nodes = nx.nodes(self.G)
            nodelist = list (nodes)
            #print (nodes)
            print(nodelist[ ind['ind'][0] ])
            self.showdialog()
            print()
            #print('cont: ' + str(cont) )

    def showdialog(self):
        d = QDialog()

        okButton = QPushButton("OK", d)
        #ledit = QLineEdit()
        #label = QLabel("Node property: ")
        #b1.move(50, 50)

        formGroupBox = QGroupBox("Form layout")
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Line 1:"), QLineEdit() )
        formLayout.addRow(QLabel("Line 2, long text:"), QComboBox() )
        formLayout.addRow(QLabel("Line 3:"), QSpinBox() )
        formGroupBox.setLayout(formLayout);

        layout = QVBoxLayout()
        layout.addWidget(formGroupBox)
        layout.addWidget(okButton)

        d.setLayout(layout)
        d.setWindowTitle("Dialog")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "TextLabel"))
        #self.label_2.setText(_translate("MainWindow", "TextLabel"))

    # def drawNodes(self, numOfNodes):
    #     self.label_list = []
    #     for k in range(numOfNodes):
    #         self.label = QtWidgets.QLabel(self.centralwidget)
    #         #self.label.setGeometry(QtCore.QRect(30+(80*k), 30, 60, 60))
    #         #self.label.setGeometry(QtCore.QRect(self.mainX/2 + (80 * k), self.mainY/2, self.nodeRadius*2, self.nodeRadius*2))
    #
    #         x = self.mainX/2 - self.nodeRadius +  (self.nodeSpacing * k)
    #         y = self.mainY/2 - self.nodeRadius
    #         width = self.nodeDiam + 1   # offset needed to fully contain the circle
    #         height = self.nodeDiam + 1  # offset needed to fully contain the circle
    #         #print (x,y,width,height)
    #         self.label.setGeometry(QtCore.QRect(x, y, width, height))
    #         self.label.setObjectName("label" + str(k))
    #
    #         pixmap = QtGui.QPixmap(width, height)
    #         #pixmap.fill(QtGui.QColor("gray"))
    #         pixmap.fill(self.centralwidget.palette().color(QPalette.Background))
    #
    #         painter = QtGui.QPainter()
    #         painter.begin(pixmap)
    #         painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0 ,255)))
    #         painter.drawEllipse(0, 0, self.nodeDiam, self.nodeDiam)
    #         #painter.fillRect(pixmap.rect(), QtGui.QColor(174, 167, 159 ,255))
    #         painter.end()
    #         self.label.setPixmap(pixmap)
    #         #self.label.setScaledContents(True)
    #         self.label_list.append(self.label)

    # def drawNodesInMap(self, relationList, nodeMap):
    #
    #     for k in range (self.label_list.__len__()):
    #         self.label_list[k].deleteLater()
    #
    #     self.label_list = []
    #
    #     xMapSize = nodeMap.size()[0]
    #     yMapSize = nodeMap.size()[1]
    #     self.currentNumOfNodes = 0
    #     for row in range( xMapSize ):
    #         for col in range( yMapSize ):
    #             if (nodeMap[godel(row, col)]) == 1 :
    #                 self.currentNumOfNodes += 1
    #                 self.label = QtWidgets.QLabel(self.centralwidget)
    #                 # self.label.setGeometry(QtCore.QRect(30+(80*k), 30, 60, 60))
    #                 # self.label.setGeometry(QtCore.QRect(self.mainX/2 + (80 * k), self.mainY/2, self.nodeRadius*2, self.nodeRadius*2))
    #
    #                 # x = self.mainX / 2 - self.nodeRadius + (self.nodeSpacing * k)
    #                 # y = self.mainY / 2 - self.nodeRadius
    #                 x = (col+1)*self.nodeRadius + (col)*self.nodeSpacing
    #                 y = (row + 1) * self.nodeRadius + (row) * self.nodeSpacing
    #
    #                 width = self.nodeDiam + 1  # offset needed to fully contain the circle
    #                 height = self.nodeDiam + 1  # offset needed to fully contain the circle
    #                 # print (x,y,width,height)
    #                 self.label.setGeometry(QtCore.QRect(x, y, width, height))
    #                 k = row * yMapSize + col
    #                 self.label.setObjectName("label" + str(k))
    #
    #                 pixmap = QtGui.QPixmap(width, height)
    #                 # pixmap.fill(QtGui.QColor("gray"))
    #                 pixmap.fill(self.centralwidget.palette().color(QPalette.Background))
    #
    #                 painter = QtGui.QPainter()
    #                 painter.begin(pixmap)
    #                 painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 255)))
    #                 painter.drawEllipse(0, 0, self.nodeDiam, self.nodeDiam)
    #                 #painter.fillRect(pixmap.rect(), QtGui.QColor(174, 167, 159 ,255))
    #                 painter.end()
    #                 self.label.setPixmap(pixmap)
    #                 # self.label.setScaledContents(True)
    #                 self.label_list.append(self.label)
    #
    #
    #
    #     for k in range(self.label_list.__len__()):
    #         self.label_list[k].show()

     # def redrawNodes(self, i):
     #    #self.drawNodes( int(self.text) )
     #
     #    # for k in range(self.totalNodes):
     #    #     self.label_list[k].hide()
     #
     #    #self.label_list[int(self.text)].hide()
     #    for k in range (self.currentNumOfNodes):
     #        self.label_list[k].deleteLater()
     #
     #    # getting number from LineEdit. currentNumOfNodes is then updated
     #    # self.currentNumOfNodes = int(self.lineEdit.text())
     #    # self.drawNodes(self.currentNumOfNodes)
     #    self.currentNumOfNodes = i
     #    self.drawNodes(self.currentNumOfNodes)
     #
     #    for k in range(self.currentNumOfNodes):
     #        self.label_list[k].show()

    # def nodeVisualizerTest(self):
    #     relationList, nodeMap = self.nodeMappingTest()
    #     self.drawNodesInMap(relationList, nodeMap)

    # Running task
    # def nodeVisualizerTask(self, serialPort):
    #
    #     # relation_list = nodeMapping.recursive_node_mapping()
    #     # self.drawLine(relation_list)
    #     # self.drawNodes(relation_list)
    #
    #     # UNCOMMENT 'while' for use in threading mode
    #     while True:
    #         #lock = threading.Lock()
    #         #lock.acquire()
    #         jsonString = serialPort.read_json_string()  # read a '\n' terminated line
    #         if jsonString != None:
    #             print (jsonString)
    #         #nodeMapping.recursive_node_mapping(jsonString)
    #         # print (line)
    #         # lock.release()
    #         # print (line)
    #         # if line:  # check if the serial bytes is not empty
    #         #     line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))  # only take JSON strings
    #         #     if (line_json != None):
    #         #         # lock.acquire()
    #         #         print( line_json.group(1) )
    #         #         # lock.release()
    #         # time.sleep(0.5)         # when it is not a JSON string
    #         # else:
    #         #     return None
    #         # if (line_json != None):
    #         #     lock.acquire()
    #         #     print( line_json.group(1) )
    #         #     lock.release()
    #         time.sleep(0.5)

    # def run_node_visualizer_thread(self, serialPort):
    #     # serial_port = serial.Serial(self.comPort, self.baudRate, timeout=0)
    #     # thread = threading.Thread(target=self.read_from_port, args=(serial_port,))     # example, with args
    #     thread = threading.Thread(target=self.nodeVisualizerTask, args=(serialPort,))
    #     thread.start()

    def setupPlot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]
        #
        # # instead of ax.hold(False)
        # # self.figure.clear()
        # #
        # # # create an axis
        # # ax = self.figure.add_subplot(111)
        # #
        # # # discards the old graph
        # # # ax.hold(False) # deprecated, see above
        # #
        # # # plot data
        # # ax.plot(data, '*-')
        # #
        # # # refresh canvas
        # # self.canvas.draw()
        #
        #self.G.add_node(1)
        graph = [(202, 213), (2177, 2299), (22, 23), (23, 24), (24, 25), (25, 20)]
        # extract nodes from graph
        nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
        # create networkx graph
        self.G = nx.Graph()

        # add nodes
        for node in nodes:
            self.G.add_node(node)

        # add edges
        for edge in graph:
            self.G.add_edge(edge[0], edge[1])

        self.pos = nx.shell_layout(self.G)

        cf, node_collection = nx.draw(self.G, self.pos)

        return cf, node_collection

    def redrawMesh(self, graph):

        self.figure.clear()

        # self.G.add_edge(self.i, self.i+1)
        # self.i += 1
        self.G = graph
        val_map = {'I am here': 'gold'}
        values = [val_map.get(node, 'violet') for node in self.G.nodes()]

        self.pos = nx.spring_layout(self.G)
        cf, node_collection = nx.draw(self.G, self.pos, node_size=500, with_labels=True, node_color=values, width=1, edge_color='lightblue',
                     font_weight='regular', font_family='Trebuchet MS', font_color='black')
        self.canvas.figure = cf
        self.node_collection = node_collection  # used for checking whether mouse click event is in a node

        self.canvas.draw()

class GetMeshFromSerialThread(QtCore.QThread):
    #updateNode = QtCore.pyqtSignal(int)
    updateNode = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.i = 1
        self.serialPort = Serial()
        self.oldJsonString = None

    # def nodeMappingTest(self):
    #     size = 11
    #     nodeMapObj = NodeMapping(size, size)
    #     initNode = [int(size / 2), int(size/ 2)]                    # initial node position
    #     initDirection = [0, 1]                                      # initial direction vector
    #     nodeMap = BitArray2D(rows=size, columns=size)    # create 2D bit array of node map
    #     nodeMap[int(size / 2), int(size / 2)] = 1                   # initialize the starting node position at the window CENTER
    #     relationList = []                                           # list holding all relations
    #
    #     jsonString = json.loads(NodeMapping.meshTopo)
    #     nodeMapObj.recursive_node_mapping(jsonString, initNode, initDirection, nodeMap, relationList)
    #     return relationList, nodeMap
    def getSerialSetting(self):
        return self.serialPort.getSerialSetting()

    def updateNetworkxGraph(self, meshString):

        graph = nx.Graph()
        jsonString = json.loads(meshString)
        recursive_node_mapping(jsonString, 'I am here', graph)

        return graph


    def run(self):

        while True:

            while True:
                jsonString = self.serialPort.read_json_string()  # read a '\n' terminated line
                #print (jsonString)
                if jsonString != None:
                    break
                #self.sleep(0.1)
            #if jsonString != None:
            self.serialPort.ser.flushInput()

            # uncomment to deliberately redraw mesh every time serial is received
            #self.oldJsonString = None
            if self.oldJsonString != jsonString:
                print(jsonString)
                graph = self.updateNetworkxGraph(jsonString)
                self.oldJsonString = jsonString
                self.updateNode.emit(graph)

                self.sleep(1)
            #self.sleep(1)
            # relationList, nodeMap = self.nodeMappingTest()

            # self.i += 1
            # self.updateNode.emit(self.i)
            # self.sleep(3)



# class ChangeNodeThread(QtCore.QThread):
#     updateNode = QtCore.pyqtSignal(int)
#
#     def __init__(self):
#         QtCore.QThread.__init__(self)
#         self.i = 1
#
#     def run(self):
#         while True:
#             self.i += 1
#             self.updateNode.emit(self.i)
#             self.sleep(3)



# """
# Initializing serial port.
# :return: serialObj
# """
# def init_serial(self, comPort=None, baudRate=115200):
#     serialObj = Serial(comPort, baudRate)
#     return serialObj

# test = Ui_MainWindow()
# relationList, nodeMap = test.nodeMapping()
# print (relationList)
# print (nodeMap)
#
# for x in range(nodeMap.size()[0]):
#     for y in range(nodeMap.size()[1]):
#         print (nodeMap[ godel(x,y)])
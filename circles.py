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

import dialog
import serial_util as su
from node_mapping import recursive_node_mapping
import json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import networkx as nx

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ESP8266 Mesh Network Visualizer")
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

        # init and open serial port
        self.ser_ref = su.init_serial(comPort='COM31')

        # References of dialog boxes appearing upon clicking nodes
        self.singleDial = None
        self.bcDial = None

        # create a thread to read from serial:
        # - for checking mesh topology changes. whenever there is a change, the mesh is redrawn
        # - for receiving replies from other nodes
        ser_read_thread = SerialThread(self.ser_ref)
        ser_read_thread.updateNodeSig.connect(self.redrawMesh)
        ser_read_thread.queryReplySig.connect(self.forwardQueryReply)
        ser_read_thread.myFreeMemSig.connect(self.forwardMyFreeMem)
        ser_read_thread.start()

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
        serialSetting = 'Port: ' + str(self.ser_ref.port) + '. Baud rate: ' + str(self.ser_ref.baudrate)
        self.serialSettingLabel.setText(serialSetting)

        # create a test button
        self.testButton = QPushButton()
        self.testButton.setText('Test Button')
        self.testButton.clicked.connect(self.write_serial)


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
        layout.addWidget(self.testButton)
        layout.addWidget(self.serialSettingLabel)
        self.centralwidget.setLayout(layout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
        #graph = [202]
        # extract nodes from graph
        #nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
        # create networkx graph
        self.G = nx.Graph()
        self.G.add_node(1)
        # add nodes
        # for node in nodes:
        #     self.G.add_node(node)

        # add edges
        # for edge in graph:
        #     self.G.add_edge(edge[0], edge[1])

        #self.pos = nx.shell_layout(self.G)

        cf, node_collection = nx.draw(self.G)

        return cf, node_collection

    # on clicking UI
    def onclick(self,event):
        cont, ind = self.node_collection.contains(event)
        # when a node is clicked
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
            nodeId = nodelist[ ind['ind'][0] ]
            print( nodeId )

            if nodeId=='Me':
                #self.showdialogBroadcast( nodeId )
                self.bcDial = dialog.BroadcastDialog()
                self.bcDial.popUp(self.ser_ref,nodeId)
            else:
                #self.showdialogSingle( nodeId )
                self.singleDial = dialog.SingleDialog()
                self.singleDial.popUp(self.ser_ref, nodeId)

            #print('cont: ' + str(cont) )

    def forwardQueryReply(self, queryReply):
        self.singleDial.query_reply(queryReply)

    def forwardMyFreeMem(self, freeMemMsg):
        self.bcDial.displayMyFreeMem(freeMemMsg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESP8266 Mesh Network Visualizer"))
        #self.label.setText(_translate("MainWindow", "TextLabel"))
        #self.label_2.setText(_translate("MainWindow", "TextLabel"))

    def write_serial(self):
        self.ser_ref.write(b'{ "dest-id":2147321632, "query":["temp", "time", "date"] }\n')

    def redrawMesh(self, graph):

        self.figure.clear()

        # self.G.add_edge(self.i, self.i+1)
        # self.i += 1
        self.G = graph
        val_map = {'Me': 'gold'}
        values = [val_map.get(node, 'violet') for node in self.G.nodes()]

        self.pos = nx.spring_layout(self.G)
        cf, node_collection = nx.draw(self.G, self.pos, node_size=500, with_labels=True, node_color=values, width=1, edge_color='lightblue',
                     font_weight='regular', font_family='Trebuchet MS', font_color='black')
        self.canvas.figure = cf
        self.node_collection = node_collection  # used for checking whether mouse click event is in a node

        self.canvas.draw()

class SerialThread(QtCore.QThread):
    #updateNode = QtCore.pyqtSignal(int)
    updateNodeSig = QtCore.pyqtSignal(object)
    queryReplySig = QtCore.pyqtSignal(object)
    myFreeMemSig = QtCore.pyqtSignal(object)

    def __init__(self, ser_ref):
        QtCore.QThread.__init__(self)
        self.i = 1
        self.serialPort = ser_ref
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
    # def getSerialSetting(self):
    #     return self.serialPort.getSerialSetting()

    def updateNetworkxGraph(self, meshString):

        graph = nx.Graph()
        try:
            jsonString = json.loads(meshString)
        except ValueError:
            print('Not a valid JSON Object')

        if (jsonString.__len__() == 0):
            graph.add_node('Me')
        else:
            recursive_node_mapping(jsonString, 'Me', graph)

        return graph


    def run(self):

        while True:

            while True:
                msgType, jsonString = su.read_json_string(self.serialPort)  # read a '\n' terminated line
                if jsonString != None:
                    break
                #self.sleep(0.1)
                #print('in serial_read_thread')
            #if jsonString != None:
            #self.serialPort.ser.flushInput()        #TODO: may be deleted, because there are several JSON strings: meshTopology, node replies

            # uncomment to deliberately redraw mesh every time serial is received
            #self.oldJsonString = None

            #TODO: check what kind of JSON string: meshTopology, nodeReply, etc.
            #print(jsonString)
            if (msgType == 'MeshTopology'):
            #if (True):
                #if "subs" in jsonString:    # it is meshTopology
                if self.oldJsonString != jsonString:
                    #print(jsonString)

                    graph = self.updateNetworkxGraph(jsonString)
                    self.oldJsonString = jsonString
                    self.updateNodeSig.emit(graph)

                    self.sleep(1)

            elif (msgType == 'query-reply'):
                self.queryReplySig.emit(jsonString)
                #self.sleep(1)

            elif (msgType == 'myFreeMem'):
                self.myFreeMemSig.emit(jsonString)
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
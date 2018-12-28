# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.5.1

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import dialog
import serial_util as su
from node_mapping import recursive_node_mapping
import json

# For embedding matplotlib(used for plotting NetworkX graph) navigation toolbar on our app window
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

        self.figure, self.node_collection = self.setupPlot()  # yoppy

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
        # SET COMxx to the corresponding serial port number used by the ESP
        self.comPortNum = 'COM31'
        self.ser_ref = su.init_serial(comPort=self.comPortNum)

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

        # For testing purpose, define a lineEdit. It accepts only 2-digit numeric
        # It was used to test redrawing number of circles according to the number given in the lineEdit
        # Not used anymore
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setMaxLength(2)
        self.lineEdit.setAlignment(Qt.AlignLeft)
        self.lineEdit.setValidator(QIntValidator())
        # Setting a connection between slider position change and on_changed_value function
        # self.lineEdit.returnPressed.connect(self.redrawMesh)

        # define label for showing serial port settings
        self.serialSettingLabel = QLabel(self.centralwidget)
        serialSetting = 'Port: ' + str(self.ser_ref.port) + '. Baud rate: ' + str(self.ser_ref.baudrate)
        self.serialSettingLabel.setText(serialSetting)

        # Create a test button
        # Used for sending commands to serial port
        self.testButton = QPushButton()
        self.testButton.setText('Test Button')
        self.testButton.clicked.connect(self.write_serial)

        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 25))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

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

        # draw() is in nx_pylab.py
        # By default draw() returns nothing. draw() is modified to return cf & node_collection
        # Because we need cf (plot figure reference) here to embed it on our top app window
        # node_collection is used when we need to detect whether a node is clicked
        cf, node_collection = nx.draw(self.G)

        return cf, node_collection

    # on clicking UI
    # We want to detect when a node on the plot is clicked. Just a simple interactive session.
    # If node 'Me' is clicked, open Broadcast dialog box which send/read to all other nodes
    # Other than node 'Me', meaning we want to interact with that particular node
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

    # Not sure if this is the best way
    # To forward signal from class SerialThread to class SingleDialog
    def forwardQueryReply(self, queryReply):
        self.singleDial.query_reply(queryReply)

    # To forward signal from class SerialThread to class BroadcastDialog
    def forwardMyFreeMem(self, freeMemMsg):
        self.bcDial.displayMyFreeMem(freeMemMsg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESP8266 Mesh Network Visualizer"))
        #self.label.setText(_translate("MainWindow", "TextLabel"))
        #self.label_2.setText(_translate("MainWindow", "TextLabel"))

    # For testing purpose. Execute this function when the Test button is pressed.
    def write_serial(self):
        self.ser_ref.write(b'{ "dest-id":2147321632, "query":["temp", "time", "date"] }\n')

    def redrawMesh(self, graph):

        self.figure.clear()

        self.G = graph
        val_map = {'Me': 'gold'}

        # If node 'Me' exists, use 'gold'. Otherwise 'violet'
        values = [val_map.get(node, 'violet') for node in self.G.nodes()]

        self.pos = nx.spring_layout(self.G)

        # This NetworkX draw() is modified to return cf and node_collection. By default, return nothing.
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

        # If mesh string is empty, draw node 'Me' only
        if (jsonString.__len__() == 0):
            graph.add_node('Me')
        else:
            recursive_node_mapping(jsonString, 'Me', graph)

        return graph


    def run(self):

        while True:

            # Wait for new string from serial port
            while True:
                msgType, jsonString = su.read_json_string(self.serialPort)  # read a '\n' terminated line
                if jsonString != None:
                    break

            # Please uncomment to deliberately redraw mesh every time serial is received
            # Otherwise, the figure is only redrawn when there is a change in the mesh topology
            #self.oldJsonString = None

            if (msgType == 'MeshTopology'):
                # Check if the mesh topology has changed
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




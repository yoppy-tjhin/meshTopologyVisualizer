
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *

import serial_util as su
import json
class BroadcastDialog:
    def __init__(self):
        self.timerLE = QLineEdit()
        self.timerLE.setValidator(QIntValidator(0, 1001))
        self.brightLE = QLineEdit()
        self.brightLE.setValidator(QIntValidator(0, 101))

    def popUp(self,serialRef, nodeId ):
        d = QDialog()
        doneButton = QPushButton("Done", d)
        doneButton.clicked.connect(lambda: self.doneBtnClicked(d))

        setFormGroupBox = QGroupBox("Set Parameters of All Nodes")      # TODO: including Me
        setFormLayout = QFormLayout()
        setFormLayout.addRow(QLabel("Timer (minutes):"), self.timerLE)
        setFormLayout.addRow(QLabel("Brightness (0-100%):"), self.brightLE)
        setBtn = QPushButton("Set")
        setFormLayout.addRow(setBtn)
        setFormGroupBox.setLayout(setFormLayout)
        setBtn.clicked.connect(lambda: self.set_write_serial(serialRef))

        queryFormGroupBox = QGroupBox("Query Parameters of All Nodes")  # TODO: including Me
        queryFormLayout = QFormLayout()
        timerLabel = QLabel()
        brightLabel = QLabel()
        queryBtn = QPushButton("Query")
        queryFormLayout.addRow(QLabel("Timer:"), timerLabel)
        queryFormLayout.addRow(QLabel("Brightness:"), brightLabel)
        queryFormLayout.addRow(queryBtn)
        queryFormGroupBox.setLayout(queryFormLayout)
        queryBtn.clicked.connect(lambda: self.query_write_serial(serialRef))

        layout = QVBoxLayout()
        layout.addWidget(setFormGroupBox)
        layout.addWidget(queryFormGroupBox)
        layout.addWidget(doneButton)

        d.setLayout(layout)
        d.setWindowTitle("Broadcast to all nodes via " + str(nodeId) )
        d.setWindowModality(Qt.ApplicationModal)
        d.resize(300, 100)
        d.exec_()

    def doneBtnClicked(self,widget):
        print ("Done button clicked")
        widget.close()

    def set_write_serial(self, serRef):
        timer = self.timerLE.text()
        brightness = self.brightLE.text()
        if (timer.__len__() != 0 and brightness.__len__() != 0):
            #dump python dictionaries to json string
            timer = int(timer)
            brightness = int(brightness)
            msgDict = {"dest-id":1, "set": {"timer": timer, "brightness": brightness}}
            # msg  = "{ \"id\":1, \"set\":{ \"timer\": %s, \"brightness\": %s }}"%(timer, bright)
            msgStr = json.dumps(msgDict) + "\n"
            msgStr = msgStr.encode('iso-8859-15')
            print(msgStr)
            serRef.write(msgStr)
        else:
            print ('Please fill both fields')

    def query_write_serial(self, serRef):
        msgDict = {"dest-id":1, "query":["timer", "brightness"]}
        msgStr = json.dumps(msgDict) + "\n"
        msgStr = msgStr.encode('iso-8859-15')
        # msg = b'{ "id":1, "set":["Node name", "Brightness"] }\n'
        print(msgStr)
        serRef.write(msgStr)

class SingleDialog:
    def __init__(self):
        self.timerLE = QLineEdit()
        self.timerLE.setValidator(QIntValidator(0, 1001))
        self.brightLE = QLineEdit()
        self.brightLE.setValidator(QIntValidator(0, 101))

    def popUp(self,serialRef, nodeId ):
        d = QDialog()
        doneButton = QPushButton("Done", d)
        doneButton.clicked.connect(lambda: self.doneBtnClicked(d))

        setFormGroupBox = QGroupBox("Set Parameters of " + str(nodeId))
        setFormLayout = QFormLayout()
        setFormLayout.addRow(QLabel("Timer (minutes):"), self.timerLE)
        setFormLayout.addRow(QLabel("Brightness (0-100%):"), self.brightLE)
        setBtn = QPushButton("Set")
        setFormLayout.addRow(setBtn)
        setFormGroupBox.setLayout(setFormLayout)
        setBtn.clicked.connect(lambda: self.set_write_serial(serialRef, nodeId))

        queryFormGroupBox = QGroupBox("Query Parameters of " + str(nodeId))
        queryFormLayout = QFormLayout()
        timerLabel = QLabel()
        brightLabel = QLabel()
        queryBtn = QPushButton("Query")
        queryFormLayout.addRow(QLabel("Timer:"), timerLabel)
        queryFormLayout.addRow(QLabel("Brightness:"), brightLabel)
        queryFormLayout.addRow(queryBtn)
        queryFormGroupBox.setLayout(queryFormLayout)
        queryBtn.clicked.connect(lambda: self.query_write_serial(serialRef, nodeId))

        layout = QVBoxLayout()
        layout.addWidget(setFormGroupBox)
        layout.addWidget(queryFormGroupBox)
        layout.addWidget(doneButton)

        d.setLayout(layout)
        d.setWindowTitle("Talk to " + str(nodeId) )
        d.setWindowModality(Qt.ApplicationModal)
        d.resize(300, 100)
        d.exec_()

    def doneBtnClicked(self,widget):
        print ("Done button clicked")
        widget.close()

    def set_write_serial(self, serRef, nodeId):
        timer = self.timerLE.text()
        bright = self.brightLE.text()
        if (timer.__len__() != 0 and bright.__len__() != 0):
            timer = int(timer)
            bright = int(bright)
            msgDict = {"dest-id": nodeId, "set": {"timer": timer, "brightness": bright}}
            # msg  = "{ \"id\":1, \"set\":{ \"timer\": %s, \"brightness\": %s }}"%(timer, bright)
            msgStr = json.dumps(msgDict) + "\n"
            msgStr = msgStr.encode('iso-8859-15')
            print(msgStr)
            serRef.write(msgStr)

        else:
            print('Please fill both fields')

    def query_write_serial(self, serRef, nodeId):
        msgDict = {"dest-id": nodeId, "query": ["timer", "brightness"]}
        msgStr = json.dumps(msgDict) + "\n"
        msgStr = msgStr.encode('iso-8859-15')
        # msg = b'{ "id":1, "set":["Node name", "Brightness"] }\n'
        print(msgStr)
        serRef.write(msgStr)

        #msg = "{ \"id\":%s, \"query\":[\"timer\", \"brightness\"] }" % (nodeId)

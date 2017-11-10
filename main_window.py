import re, sys, time, threading
import serial

from PyQt5 import QtCore, QtGui, QtWidgets
from circles import Ui_MainWindow
from firstgui import Ui_myfirstgui

#from myform import Ui_Dialog
#from button_grid2 import Ui_Dialog


# class MyFirstGuiProgram(Ui_myfirstgui):
#     def __init__(self, dialog):
#         Ui_myfirstgui.__init__(self)
#         self.setupUi(dialog)
#
#         # Connect "add" button with a custom function (addInputTextToListbox)
#         self.addBtn.clicked.connect(self.addInputTextToListbox)
#
#     def addInputTextToListbox(self):
#         txt = self.myTextInput.text()
#         self.listWidget.addItem(txt)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

class Serial():

    def read_from_port(self, ser):
        while True:
            lock = threading.Lock()
            lock.acquire()
            line = ser.readline()  # read a '\n' terminated line
            #print (line)
            lock.release()
            time.sleep(0.5)
            #print (line)
            if line:
                #print(line.decode('utf-8'))
                line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))
                if (line_json != None):
                    lock.acquire()
                    print( line_json.group(1) )
                    lock.release()
                #print(line)


    def run_serial_thread(self):
        serial_port = serial.Serial('COM13', 115200, timeout=0)
        thread = threading.Thread(target=self.read_from_port, args=(serial_port,))
        thread.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    serialPort = Serial()
    serialPort.run_serial_thread()
    sys.exit(app.exec_())


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     dialog = QtWidgets.QDialog()
#
#     #prog = MyFirstGuiProgram(dialog)
#     prog = MyFirstGuiForm(dialog)
#
#     dialog.show()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        #windowLayout = QVBoxLayout()
        #windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.layout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        self.layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        self.layout.addWidget(QPushButton('1'), 0, 0)
        self.layout.addWidget(QPushButton('2'), 0, 1)
        self.layout.addWidget(QPushButton('3'), 0, 2)
        self.layout.addWidget(QPushButton('4'), 1, 0)
        self.layout.addWidget(QPushButton('5'), 1, 1)
        self.layout.addWidget(QPushButton('6'), 1, 2)
        self.layout.addWidget(QPushButton('7'), 2, 0)
        self.layout.addWidget(QPushButton('8'), 2, 1)
        self.layout.addWidget(QPushButton('9'), 2, 2)

        #self.horizontalGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
#from circles import Ui_MainWindow
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


class MyFirstGuiForm(Ui_myfirstgui):
    def __init__(self, dialog):
        Ui_myfirstgui.__init__(self)
        self.setupUi(dialog)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    #prog = MyFirstGuiProgram(dialog)
    prog = MyFirstGuiForm(dialog)

    dialog.show()
    sys.exit(app.exec_())

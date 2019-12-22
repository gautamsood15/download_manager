from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType


ui , _ = loadUiType('main.ui')    #convert UI file to python file

class MainApp(QMainWindow , ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)     #application can have many windows, this is an object of QApplication
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

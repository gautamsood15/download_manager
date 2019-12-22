from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType

ui, _ = loadUiType('main.ui')  # convert UI file to python file


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_Buttons()

        '''InitUI and Handle_Buttons 
        are placed here to run when the code is executed'''

    def InitUI(self):  # contain all ui changes in loading
        pass

    def Handel_Buttons(self):  # handel all buttons in the app
        self.pushButton.clicked.connect(self.Download)

    def Handle_progress(self):  # calculate the progress
        pass

    def Handle_Browse(self):  # enable browsing to our os , pick save location
        pass

    def Download(self):  # downloading any file
        print('Starting Download')

    def Save_Browse(self):  # save location in the line edit
        pass


def main():
    app = QApplication(sys.argv)  # application can have many windows, this is an object of QApplication
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

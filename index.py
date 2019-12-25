from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
# Make sure to install youtube-dl



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
        self.pushButton_2.clicked.connect(self.Handle_Browse)

        self.pushButton_5.clicked.connect(self.Get_Video_Data)




    def Handle_progress(self , blocknum , blocksize , totalsize):  # calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()            # Makes ui more responsive and not allow to freeze



    def Handle_Browse(self):  # enable browsing to our os , pick save location

        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files (*.*)")

        self.lineEdit_2.setText(str(save_location[0]))




    def Download(self):     # downloading any file
        print('Starting Download')

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '':
            QMessageBox.warning(self , "Data Error" , "Provide a url")

        if save_location == '':
            QMessageBox.warning(self , "Data Error" , "Provide a save location")
        else:
            try:
                urllib.request.urlretrieve(download_url , save_location , self.Handle_progress)

            except Exception:
                QMessageBox.warning(self , "Download Error" , "Provide a valid url")
                return

        QMessageBox.information(self , "Donwload Completed" , "The File is Saved Successfully")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Browse(self):  # save location in the line edit
        pass



##############################################################
#################  Download Youtube Single Video

    def Get_Video_Data(self):

        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self , "Data Error" , "Provide a video url")

        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

        






    def Download_Video(self):
        pass

    def Video_Progress(self):
        pass


def main():
    app = QApplication(sys.argv)  # application can have many windows, this is an object of QApplication
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

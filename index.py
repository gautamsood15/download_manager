from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
# Make sure to install youtube-dl
import humanize



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

        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)


################################## TAB 1 - DOWNLOAD FILES ################################################


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



    ################################## TAB 2 - SINGLE FILES ################################################



    def Save_Browse(self):  # save location form os in the line edit for video
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files (*.*)")
        self.lineEdit_4.setText(str(save_location[0]))


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

            video_streams = video.allstreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = " {} | {} | {} | {} ".format(stream.mediatype , stream.extension , stream.quality , size)
                self.comboBox.addItem(data)


    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '':
            QMessageBox.warning(self , "Data Error" , "Provide a url")

        if save_location == '':
            QMessageBox.warning(self , "Data Error" , "Provide a save location")
        else:
            video = pafy.new(video_url)
            video_stream = video.allstreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location , callback=self.Video_Progress)





    def Video_Progress(self , total , received , ratio , rate , time):
        readed_data = received
        if total > 0:
            download_precentage = readed_data * 100 / total
            self.progressBar_2.setValue(download_precentage)
            remaning_time = round(time/60 , 2)

            self.label_5.setText(str('{} minutes remaning').format(remaning_time))
            QApplication.processEvents()




################################## TAB 2 - FULL PLAYLIST ################################################















def main():
    app = QApplication(sys.argv)  # application can have many windows, this is an object of QApplication
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

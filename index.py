from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
# Make sure to install youtube-dl
import humanize
import os
from os import path




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
        self.tabWidget.tabBar().setVisible(False)

        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()



    def Handel_Buttons(self):  # handel all buttons in the app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)

        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)

        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_8.clicked.connect(self.Playlist_Save_Browse)

        self.pushButton_6.clicked.connect(self.Open_Home)
        self.pushButton_11.clicked.connect(self.Open_Download)
        self.pushButton_10.clicked.connect(self.Open_Youtube)
        self.pushButton_9.clicked.connect(self.Open_Settings)

        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_DarkBlue_Style)
        self.pushButton_16.clicked.connect(self.Apply_Classic_Style)




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
            video_stream[video_quality].download(filepath=save_location , callback=self.Video_Progress)





    def Video_Progress(self , total , received , ratio , rate , time):
        readed_data = received
        if total > 0:
            download_precentage = readed_data * 100 / total
            self.progressBar_2.setValue(download_precentage)
            remaning_time = round(time/60 , 2)

            self.label_5.setText(str('{} minutes remaning').format(remaning_time))
            QApplication.processEvents()




################################## TAB 2 - FULL PLAYLIST ################################################


    def Playlist_Download(self):

        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a url")

        if save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()


        QApplication.processEvents()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.allstreams
            self.lcdNumber.display(current_video_in_download)
            current_video_stream[quality].download(callback=self.Playlist_Progress)
            current_video_in_download += 1




    def Playlist_Progress(self , total , received , ratio , rate , time):
        if total > 0:
            download_percentage = received * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60 , 2)

            self.label_3.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()



    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)




################################## UI CHANGES METHODS ################################################

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)
        



################################## APP THEMES ################################################


    def Apply_DarkOrange_Style(self):
        style = open('themes/darkorange.css' , 'r')
        style  = style.read()
        self.setStyleSheet(style)


    def Apply_QDark_Style(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Classic_Style(self):
        style = open('themes/classic.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkBlue_Style(self):
        style = open('themes/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)




############################### APP ANIMATION ################################################

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox , b"geometry")
        box_animation1.setDuration(1000)  #1 second
        box_animation1.setStartValue(QRect(0,0,0,0))
        box_animation1.setEndValue(QRect(30 , 20 , 351 , 131))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2 , b"geometry")
        box_animation2.setDuration(1000)  #1 second
        box_animation2.setStartValue(QRect(0,0,0,0))
        box_animation2.setEndValue(QRect(430 , 20 , 351 , 131))
        box_animation2.start()
        self.box_animation2 = box_animation2





def main():
    app = QApplication(sys.argv)  # application can have many windows, this is an object of QApplication
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

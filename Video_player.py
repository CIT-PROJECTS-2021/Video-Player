from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowIcon(QIcon("logoo.ico"))
        self.setWindowTitle("Group7 Video Player")
        self.setGeometry(350, 100, 700,500)


        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.create_player()


    def create_player(self):


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        video_widget = QVideoWidget()

        self.open_Btn = QPushButton("Open Video")
        #self.open_Btn.setEnabled(False)
        self.open_Btn.clicked.connect(self.open_file)

        # self.yt_btn = QPushButton("YT")
        # self.yt_btn.clicked.connect(self.addWebVideo)

        
        
        self.play_Btn = QPushButton()
        self.play_Btn.setEnabled(False)
        # Using PyQt icons library
        self.play_Btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_Btn.clicked.connect(self.play_video)


        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)



        hbox = QHBoxLayout()   # Align widgets Horizontally
        hbox.setContentsMargins(0,0,0,0)

        hbox.addWidget(self.open_Btn)
        # hbox.addWidget(self.yt_btn)
        hbox.addWidget(self.play_Btn)
        hbox.addWidget(self.slider)



        vbox = QVBoxLayout()   # Align Widgets Vertically
        vbox.addWidget(video_widget)
        
        vbox.addLayout(hbox)

        # To show the output/Video
        self.mediaPlayer.setVideoOutput(video_widget)

        # Main window layout
        self.setLayout(vbox)


        self.mediaPlayer.stateChanged.connect(self.mediaState_change)

        self.mediaPlayer.positionChanged.connect(self.position_change)

        self.mediaPlayer.durationChanged.connect(self.duration_change)
        

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if file_name != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.play_Btn.setEnabled(True)



    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def mediaState_change(self,state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.play_Btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.play_Btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def position_change(self,position):
        self.slider.setValue(position)

    
    def duration_change(self, duration):
        self.slider.setRange(0, duration)

    
    def set_position(self,position):
        self.mediaPlayer.setPosition(position)

    
    # def addWebVideo(self, video_id):
    #     self.web_view = QWebEngineView()
    #     self.web_view.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
    #     self.layout.addWidget(self.web_view)

    # def update_video(self):
    #     self.video_Id = self.input.text()
    #     self.web_view.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))


app = QApplication(sys.argv)   # Object of class QApplication
window = Window()   # Instance of class Window
window.show()   # Method to show window


# To open the window
sys.exit(app.exec_())  # PyQt5   in 6 sys.exit(app.exec())
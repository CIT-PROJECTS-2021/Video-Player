from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys     
class Worker(QtCore.QObject):
    word=QtCore.pyqtSignal(str)
    def encrypt(self,path,obj):
        try:
            with open(path, 'rb') as stream:
                    obj.setData(stream.read())
            if obj.open(QtCore.QIODevice.ReadOnly):
                self.word.emit('hi')
        except Exception as e:
                print(e)        
class Player(QMainWindow):
    speak=QtCore.pyqtSignal(str,object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
#######
#Here is the main part
#####
        self.worker = Worker()
        self.speak.connect(self.worker.encrypt)
        self.thread=QtCore.QThread(self)
        self.worker.moveToThread(self.thread)
        self.worker.word.connect(self.ready)
        self.buffer = QtCore.QBuffer()
    def ready(self):
        print('Ready')  
        self.mediaPlayer.setMedia(
                    QMediaContent(), self.buffer)
                  
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                "C:/Users/mishra/Desktop/HiddenfilesWindow/")
        print(fileName)
        if fileName != '':
            try:
                self.buffer.close()
                self.thread.start()
                self.speak.emit(fileName,self.buffer)
                # self.mediaPlayer.setMedia(
                #         QMediaContent(QUrl.fromLocalFile(fileName)))
                self.playButton.setEnabled(True)
            except Exception as e:
                print(e)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
          
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Player()
    window.show()
    sys.exit(app.exec_())

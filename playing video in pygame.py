import os
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPalette


WIDTH, HEIGHT = 1920, 1200

# class Slider(QWidget):
    

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Framura Inspectura")
        # Set up the media player and video widget
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.video_widget.showMaximized()

        video_aspect_ratio = (16,9)
        botto_slider_height = HEIGHT//16

        self.setGeometry(WIDTH//3, HEIGHT//3, WIDTH//2, HEIGHT//2)
        # self.setGeometry(0,0, WIDTH, HEIGHT)
        # self.showMaximized()

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.media_player.setVideoOutput(self.video_widget)

        # Load the video file
        file_path = os.path.join("outlaw.mkv")
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

        self.color_widget = QWidget(self)
        # self.color_widget.setStyleSheet("QWidget { background-color: blue; }")
        self.media_player.positionChanged.connect(self.onPositionChanged)
        self.media_player.stateChanged.connect(self.onStateChanged)
        self.media_player.setNotifyInterval(100)

        # self.media_player.mediaStatusChanged.connect(self.onStateChanged)
        
        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(self.video_widget,stretch=31)
        vboxlayout.addWidget(self.color_widget,stretch=1)
        vboxlayout.setContentsMargins(0, 0, 0, 0)
        vboxlayout.setSpacing(2)
        self.setLayout(vboxlayout)
        self.vboxlayout = vboxlayout

        self.media_player.play()
        # self.media_player.playbackRate() #speed

        # self.media_player.positionChanged.connect(self.onPositionChanged)

    def onStateChanged(self, state):
        print("State:",state)
        if state == 0:
            print("REWIND")
            # self.media_player.setPosition(0)
            self.media_player.play()
        # if self.media_player.position == self.media_player.duration:
        #     print("finished")
        #     self.media_player.setPosition(0)
        #     self.media_player
        # print(position)
        # self.update()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print('space pressed')
            self.media_player.play() if self.media_player.state() in [0,2] else self.media_player.pause() #stopped or paused state 
        if event.key() == Qt.Key_Escape:
            self.close()

        
    def keyboardEventReceived(self, event):
        'captures input (the window is always in focus so no input can hide!)'
        if event.event_type == 'down':
            if event.name == 'space':
                print('space pressed')
                self.media_player.play() if self.media_player.state() in [0,2] else self.media_player.pause() #stopped or paused state 
                
            elif event.name == 'esc':
                self.close()


    def onPositionChanged(self, position):
        print(position)
        self.update()

        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255, 0, 0))  # Set the pen color to red
        qp.setBrush(QColor(255, 0, 0))
        rect = self.color_widget.geometry()
        multiplier =  0 if self.media_player.duration() ==0 else self.media_player.position()/self.media_player.duration()
        qp.drawRect(rect.left(),rect.top(),int(rect.width() * multiplier), rect.height())
        # qp.drawRect(0,0,1920,1000)
        qp.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
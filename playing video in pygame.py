import os
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPalette

import utils

WIDTH, HEIGHT = 1920, 1200

# class Slider(QWidget):
    

class App(QWidget):

    ####### INIT ############

    def __init__(self):
        super().__init__()

        #window options
        self.setWindowTitle("Framura Inspectura")
        self.setGeometry(WIDTH//3, HEIGHT//3, WIDTH//2, HEIGHT//2)

        #palette
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        #video widget
        self.video_widget = QVideoWidget(self)
        self.video_widget.showMaximized()

        #media player
        self.media_player = QMediaPlayer(self)
        file_path = os.path.join("outlaw.mkv")
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.onPositionChanged)
        self.media_player.stateChanged.connect(self.onStateChanged)
        self.media_player.setNotifyInterval(100)
        self.playback_speed = 1.0
        self.playback_speed_limits = (0.25, 2)
        self.media_player.play()

        #seek/status/progress bar
        self.color_widget = QWidget(self)        
        
        #layout
        vboxlayout = QVBoxLayout()
        self.vboxlayout = vboxlayout
        vboxlayout.addWidget(self.video_widget,stretch=31)
        vboxlayout.addWidget(self.color_widget,stretch=1)
        vboxlayout.setContentsMargins(0, 0, 0, 0)
        vboxlayout.setSpacing(2)
        self.setLayout(vboxlayout)


    ####### PYQTs FUNCTIONS ############

    def onStateChanged(self, state):
        'callback played when video state has changed (playing, paused, stopped)'
        #loop when video finished playing
        if state == QMediaPlayer.StoppedState:
            self.media_player.play()

    
    def keyPressEvent(self, event):
        "PyQt's keyboard pressing detection"
        #pause/unpause playback
        if event.key() == Qt.Key_Space:
            self.media_player.play() if self.media_player.state() in [0,2] else self.media_player.pause() #stopped or paused state 
        #quit application
        if event.key() == Qt.Key_Escape:
            self.close()

        #speed up
        elif event.key() == Qt.Key_Up:
            self.change_playback_rate(direction = 1)            
        #slow down
        elif event.key() == Qt.Key_Down:
            self.change_playback_rate(direction = -1)

        #step through frames when video is paused
        if self.media_player.state() == QMediaPlayer.PausedState:
            if event.key() == Qt.Key_Left:
                self.step_by_frame(direction = -1)
            if event.key() == Qt. Key_Right:
                self.step_by_frame(direction = 1)


    def mousePressEvent(self, event):
        "PyQt's mouse pressing detection"
        #change video position
        if event.button() == Qt.LeftButton:
            self.media_player.setPosition(int(utils.remap(
                event.pos().x(),
                0, self.color_widget.width(), 
                0, self.media_player.duration() )) 
                )
        #loop section
        elif event.button() == Qt.RightButton:
            pass


    def onPositionChanged(self, position):
        'callback called when video position has changed'
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

    ####### CUSTOM FUNCTIONS ############

    def change_playback_rate(self, direction=1):
        'changes the speed of playback; speeds up when "direction" is 1", slows down when -1'
        self.playback_speed += direction * 0.25
        self.playback_speed = utils.clamp(self.playback_speed, self.playback_speed_limits[0], self.playback_speed_limits[1])
        self.media_player.setPlaybackRate(self.playback_speed)
    

    def step_by_frame(self, direction=1):
        'move one frame left or right, depeneding on "direction" argument'
        new_pos = self.media_player.position() + direction
        new_pos = utils.clamp(new_pos, 0, self.media_player.duration())
        self.media_player.setPosition(new_pos)

############# MAIN ##################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
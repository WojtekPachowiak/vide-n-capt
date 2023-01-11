import os
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPalette
import tkinter as tk # for getting screen width and height
import keyboard 
import numpy as np 
import cv2 # saving screenshots to file
import pyautogui # taking screenshots
import threading
import tempfile

import utils

FPS = 60
#length of one frame in miliseconds
ONE_FRAME = 1000//FPS 


root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

TEMP_VIDEO_PATH = os.path.join(tempfile.gettempdir(), "rec.mp4") #the recording is meant to be stored temporarily


class ScreenRecorder(threading.Thread):
    'responsible for screen recording. runs in seperate thread'

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #prepare opencv's VideoWriter
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.running = False

    def run(self):
        self.running =True
        self.out = cv2.VideoWriter(TEMP_VIDEO_PATH, self.codec, FPS, (WIDTH, HEIGHT))

        while self.running:

            #make a screenshot, convert it np.array and correct opencv's default BGR color representation
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

            #write a frame to previously specified tempfile
            self.out.write(frame)

            #delay the loop to match the framerate
            cv2.waitKey(int(1/FPS*1000))

        self.out.release()
    
    def kill(self):
        self.running= False



class RecordingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, WIDTH, HEIGHT)

        self.hook = keyboard.on_press(self.keyboardEventReceived)
        self.is_recording = False
        self.recorder = ScreenRecorder()
        self.playback_app = PlaybackApp()
        self.playback_app.hide()
        

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        col = QColor(255,0,0) if self.is_recording else QColor(255,255,0)
        pen = QPen(col)
        pen.setWidth(10)
        qp.setPen(pen)
        qp.drawRect(0,0,self.width()-1,self.height()-1)
        qp.end()


    def keyboardEventReceived(self, event):
        'captures input (the window is always in focus so no input can hide!)'
        if event.event_type == 'down':
            if event.name == 'f3':
                print("f3 in RecordingApp")
                self.is_recording = not self.is_recording
                self.update()
                if self.is_recording:
                    if not self.playback_app.isHidden():
                        print("RecordingApp: stop video")
                        self.playback_app.stop_video()
                        self.playback_app.hide()
                    print("RecordingApp: start recorder")
                    self.recorder.start()
                else:
                    print("RecordingApp: kill recorder")
                    self.recorder.kill()
                    print("RecordingApp: start video")
                    self.playback_app.show()
                    self.playback_app.start_video()
                    
            elif event.name == 'esc':
                print("RecordingApp: exit")
                self.close()



class PlaybackApp(QWidget):

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
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.onPositionChanged)
        self.media_player.stateChanged.connect(self.onStateChanged)
        self.media_player.setNotifyInterval(100)
        self.playback_speed = 1.0
        self.playback_speed_limits = (0.25, 2)

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
        if event.key() == Qt.Key_F3:
            window = RecordingApp()
            window.show()
            
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
                self.move_playback_position(delta = -ONE_FRAME)
            if event.key() == Qt. Key_Right:
                self.move_playback_position(delta = ONE_FRAME)
        #jump through frames when video is paused
        else:
            if event.key() == Qt.Key_Left:
                self.move_playback_position(delta = -self.media_player.duration()//10)
            if event.key() == Qt. Key_Right:
                self.move_playback_position(delta = self.media_player.duration()//10)
        



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

    def start_video(self):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_PATH)))
        self.media_player.play()
    
    def stop_video(self):
        self.media_player.stop()



    def change_playback_rate(self, direction=1):
        'changes the speed of playback; speeds up when "direction" is 1", slows down when -1'
        self.playback_speed += direction * 0.25
        self.playback_speed = utils.clamp(self.playback_speed, self.playback_speed_limits[0], self.playback_speed_limits[1])
        self.media_player.setPlaybackRate(self.playback_speed)
    

    def move_playback_position(self, delta):
        'move one frame left or right, depeneding on "direction" argument'
        new_pos = self.media_player.position() + delta
        new_pos = utils.clamp(new_pos, 0, self.media_player.duration())
        self.media_player.setPosition(new_pos)
        self.media_player.play()




############# MAIN ##################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecordingApp()
    window.show()
    app.exec_()
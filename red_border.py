import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import tkinter as tk # for getting screen width and height
import keyboard 
import numpy as np 
import cv2 # saving screenshots to file
import pyautogui # taking screenshots
import threading
import tempfile
import os


root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()



class ScreenRecorder(threading.Thread):
    'responsible for screen recording. runs in seperate thread'

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #prepare opencv's VideoWriter
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.filename = os.join(tempfile.gettempdir(), "rec.mp4") #the recording is meant to be stored temporarily
        self.fps = 60.0
        self.running = False

    def run(self):
        self.running =True
        self.out = cv2.VideoWriter(self.filename, self.codec, self.fps, (WIDTH, HEIGHT))

        while self.running:

            #make a screenshot, convert it np.array and correct opencv's default BGR color representation
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

            #write a frame to previously specified tempfile
            self.out.write(frame)

            #delay the loop to match the framerate
            cv2.waitKey(int(1/self.fps*1000))

        self.out.release()
    
    def kill(self):
        self.running= False



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, WIDTH, HEIGHT)

        self.hook = keyboard.on_press(self.keyboardEventReceived)
        self.is_recording = False
        self.recorder = ScreenRecorder()
        

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
                print('F3 pressed')
                self.is_recording = not self.is_recording
                self.update()
                if self.is_recording:
                    self.recorder.start()
                else:
                    self.recorder.kill()
            elif event.name == 'esc':
                self.close()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
import profile
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import tkinter as tk
import keyboard

root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, WIDTH, HEIGHT)



    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(QColor(255,0,0))
        pen.setWidth(10)
        qp.setPen(pen)
        qp.drawRect(0,0,self.width()-1,self.height()-1)
        # qp.drawLine()
        qp.end()

        # qp.setPen(QColor(255, 0, 0))
        # profile.setPen(QPen(Qt::red,3,Qt::SolidLine));
        # p.drawLine(x,y,x +0,_height/4+y);
        # p.drawLine(x,y+ _height,x + 0,_height - _height/4+y);
        # p.drawLine(x,y,x +_width/4,0+y);
        # p.drawLine(x,y+_height,x +_width/4,_height+y);
        # p.drawLine(_width+x,y+_height,x +_width - _width/4,_height+y);
        # p.drawLine(_width+x,y+_height,x +_width,_height - _height/4+y);
        # p.drawLine(_width+x,y,x + _width-_width/4,0+y);
        # p.drawLine(_width+x,y,_width+x,_height/4+y);

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F3:
            print('record!!!')
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            print(f"Key press: {event.text()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())
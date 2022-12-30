from PyQt5 import QtCore, QtWidgets
import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
import sys

class KeyGrabber(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.button = QtWidgets.QPushButton('start')

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1200)

        layout.addWidget(self.button)
        self.button.setCheckable(True)
        self.button.toggled.connect(self.setGrabbing)

    def keyboardEventReceived(self, event):
        if event.event_type == 'down':
            if event.name == 'f3':
                print('F3 pressed')
            elif event.name == 'f4':
                print('F4 pressed')

    def setGrabbing(self, enable):
        if enable:
            self.button.setText('stop')
            # on_press returns a hook that can be used to "disconnect" the callback
            # function later, if required
            self.hook = keyboard.on_press(self.keyboardEventReceived)
            self.showMinimized()
        else:
            self.button.setText('start')
            keyboard.unhook(self.hook)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeyGrabber()
    window.show()
    sys.exit(app.exec_())
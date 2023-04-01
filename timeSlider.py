import sys, globals

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QSlider,
    QVBoxLayout,
    QWidget,
)

# Subclass QMainWindow to customize your application's main window
class TimeScale(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("")
        self.resize(1000,90)

        layout = QVBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        

        layout.addWidget(self.slider)

        widget = QWidget()
        widget.setLayout(layout)
        
        self.slider.valueChanged.connect(self.timejump)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def modify(self, frame):
        print(f"set slider val {frame}, peak {globals.frameMax}")
        globals.autoModify = True
        self.slider.setValue(frame)
        globals.autoModify = False
        self.slider.setMaximum(globals.frameMax)
    
    
    def timejump(self, s):
        if(not globals.autoModify):
            globals.mod(s)
            print(f"manual move, {s}, auto {globals.autoModify}")
            globals.manualModify = True


def createSlider():
    app = QApplication(sys.argv)
    sliderbar = TimeScale()
    sliderbar.show()

    app.exec()  

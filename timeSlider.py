import sys

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

        slider = QSlider(Qt.Horizontal)

        layout.addWidget(slider)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


def createSlider():
    app = QApplication(sys.argv)
    sliderbar = TimeScale()
    sliderbar.show()

    app.exec()  

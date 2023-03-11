import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import simulation

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox(),
            QComboBox(),
            QDial(),
            QDoubleSpinBox(),
            QLabel(),
            QPushButton("Enter Simulation"),
            QPushButton(),
            QRadioButton(),
            QSpinBox(),
        ]

        widgets[1].addItems(["Aluminum", "Steel", "Brass", "PLA"])

        widgets[4].setText("Choose ")
        #widgets[5].hitButton.connect( self.start_sim )

        # There is an alternate signal to send the text.
        #widgets[1].currentTextChanged.connect( self.text_changed )

        #self.setCentralWidget(widgets[1])

        widgets[8].setMinimum(10)
        widgets[8].setMaximum(1000)
        widgets[8].setSuffix("%")
        widgets[8 ].setSingleStep(10)
        #widgets[8].setDefault(100)

        widgets[0].stateChanged.connect(self.start_sim)

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
    
    def start_sim(self, s):
        simulation.runWindow()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

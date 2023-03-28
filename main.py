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

import simulation, exportData

fps = 30
material = "Aluminum6061"
test = "Tensile"

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Lab")
        self.resize(300,400)

        layout = QVBoxLayout()
        
        chooseTestType = QComboBox()
        chooseMaterial = QComboBox()
        
        dial = QDial()
        doubleSpinBox = QDoubleSpinBox()
        chooseBreakageOnlyCheckBox = QCheckBox()
        allFramesOrTimeAccurate = QCheckBox("All Frames?")
        enterSimButton = QPushButton("Enter Simulation")
        failure = QLabel()
        getDataButton = QPushButton("Get Raw Data")
        playbackSpeed = QSpinBox()
        playbackSpeedText = QLabel("Playback Speed")
        success = QLabel()

        self.successLabel = success
        self.chooseMaterialBox = chooseMaterial
        self.failureLabel = failure
        self.playbackMultiplier = playbackSpeed
        self.dialRoll = dial

        widgets = [
            chooseTestType,
            chooseMaterial,
            failure,
            dial,
            #doubleSpinBox,
            chooseBreakageOnlyCheckBox,
            enterSimButton,
            getDataButton,
            success,
            playbackSpeedText,
            playbackSpeed,
        ]

        chooseMaterial.addItems(["Aluminum 6061", "Steel 1084", "Steel 316L" , "Brass 360", "PLA"])
        chooseTestType.addItems(["Tensile", "Fatigue", "Hardness" , "Charpy"])

        chooseBreakageOnlyCheckBox.setText("Breakage Point Only")

        playbackSpeed.setMinimum(10)
        playbackSpeed.setMaximum(1000)
        playbackSpeed.setSuffix("%")
        playbackSpeed.setSingleStep(10)
        playbackSpeed.setValue(100)

        dial.setMinimum(0)
        dial.setMaximum(1000)


        enterSimButton.clicked.connect(self.start_sim)
        #enterSimButton.setStyleSheet("color: lime")

        getDataButton.clicked.connect(self.export_data)
        
        playbackSpeed.valueChanged.connect(self.fps_changed)

        chooseMaterial.currentTextChanged.connect(self.material_changed)
        chooseTestType.currentTextChanged.connect(self.test_changed)

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
    
    def start_sim(self, s):
        print(fps)
        try:
            simulation.runWindow(fps,material, test, True)
            self.failureLabel.setText("")
        except FileNotFoundError:
            self.failureLabel.setText("One or more of the videos not found")
            self.failureLabel.setStyleSheet("color:red")


    def fps_changed(self, s):
        global fps
        print("Percent",s)
        fps = 30 * s / 100
        # if(s >= 1000):
        #    self.playbackMultiplier.setSingleStep(1000)
        # el
        if(s >= 200):
            self.playbackMultiplier.setSingleStep(100)
        else:
            self.playbackMultiplier.setSingleStep(10)
        print(fps)

    def material_changed(self, s):
        global material
        material = s.replace(" ","")
        print("Material",material)
        
        #if(s > 200):
        #    playbackspeed
        #print(fps)
    
    def test_changed(self, s):
        global test, material
        test = s.replace(" ","")
        print("Test",test)
        if(test == "Tensile"):
            self.chooseMaterialBox.clear()
            self.chooseMaterialBox.addItems(["Aluminum 6061", "Steel 1084", "Steel 316L" , "Brass 360", "PLA"])
        elif(test == "Fatigue"):
            self.chooseMaterialBox.clear()
            self.chooseMaterialBox.addItems(["Steel 316L"])
        elif(test == "Hardness"):
            self.chooseMaterialBox.clear()
            self.chooseMaterialBox.addItems(["Brass 360"])
        elif(test == "Charpy"):
            self.chooseMaterialBox.clear()
            self.chooseMaterialBox.addItems(["Steel 4140"])

        

    def export_data(self, s):
        exportData.export(material)
        self.successLabel.setText("Success")
        self.successLabel.setStyleSheet("color:lime")
    
    def modifyDial(self, num):
        self.dialRoll.setValue(num)

        

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

import pip
import sys
from multiprocessing import Process
try:
    from PyQt5.QtCore import Qt
except ModuleNotFoundError: 
    pip.main(['install', 'PyQt5'])
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

#import localSimulation, 
import boto3Simulation, exportData

useAWS = True

fps = 30
material = "Aluminum6061"
test = "Tensile"
allFrames = False
#resolution = "720p"

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Lab")
        self.resize(300,400)

        layout = QVBoxLayout()
        
        chooseTestType = QComboBox()
        chooseMaterial = QComboBox()
        
        dial = QDial() #funny dial
        chooseBreakageOnlyCheckBox = QCheckBox() #breakage only timestamp
        allFramesOrTimeAccurate = QCheckBox("All Frames?") #attempt at frameskip
        enterSimButton = QPushButton("Enter Simulation") #enter simulation
        failure = QLabel() #blank label for failure
        getDataButton = QPushButton("Get Raw Data") #get data
        playbackSpeed = QSpinBox() # speed of playback
        playbackSpeedText = QLabel("Playback Speed") # label for speed of playback
        success = QLabel() #blank label for raw data success
        toggle4K = QCheckBox("4K") #4K toggle, future implementation

        #save some as class variables to use them in other functions
        self.successLabel = success
        self.chooseMaterialBox = chooseMaterial
        self.failureLabel = failure
        self.playbackMultiplier = playbackSpeed
        self.dialRoll = dial
        self.exportButton = getDataButton

        #set up widget layout
        widgets = [
            chooseTestType,
            chooseMaterial,
            failure,
            dial,
            chooseBreakageOnlyCheckBox,
            enterSimButton,
            getDataButton,
            success,
            #playbackSpeedText,
            #playbackSpeed,
            #allFramesOrTimeAccurate,
            #toggle4K
        ]
        chooseTestType.addItems(boto3Simulation.testTypes)
        
        chooseMaterial.addItems(["Aluminum 6061", "Steel 1084", "Steel 316L" , "Brass 360", "PLA"])

        chooseBreakageOnlyCheckBox.setText("Breakage Point Only")

        playbackSpeed.setMinimum(10)
        playbackSpeed.setMaximum(1000)
        playbackSpeed.setSuffix("%")
        playbackSpeed.setSingleStep(10)
        playbackSpeed.setValue(100)

        dial.setMinimum(0)
        dial.setMaximum(1000)

        allFramesOrTimeAccurate.setChecked(True)

        #connect all actions with their respective callback functions
        enterSimButton.clicked.connect(self.start_sim)

        allFramesOrTimeAccurate.stateChanged.connect(self.allFrames_changed)

        getDataButton.clicked.connect(self.export_data)
        
        playbackSpeed.valueChanged.connect(self.fps_changed)

        chooseMaterial.currentTextChanged.connect(self.material_changed)
        chooseTestType.currentTextChanged.connect(self.test_changed)

        chooseTestType.setCurrentIndex(3)
        #chooseMaterial.setCurrentIndex(3)

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
    
    def start_sim(self, s):
        global test
        
        self.failureLabel.setText("")

        try:
            if(test == "RockwellHardness"):
                test = "Hardness"
            if(useAWS):
                boto3Simulation.runWindow(fps, material, test, allFrames)
            else:
                #localSimulation.runWindow(fps, material, test, allFrames)
                print ("No local, please contact the software provider for details")
            self.failureLabel.setText("")
        except FileNotFoundError:
            self.failureLabel.setText("One or more of the videos not found")
            self.failureLabel.setStyleSheet("color:red")

    #if the allframes checkbox has changed
    def allFrames_changed(self, s):
        global allFrames
        allFrames = s

    #if the fps spinbox has changed
    def fps_changed(self, s):
        global fps

        fps = 30 * s / 100

        if(s >= 200):
            self.playbackMultiplier.setSingleStep(100)
        else:
            self.playbackMultiplier.setSingleStep(10)

    #if the material spinbox has changed
    def material_changed(self, s):
        global material
        material = s.replace(" ","")
    
    #if the test spinbox has changed
    def test_changed(self, s):
        global test, material
        test = s.replace(" ","")

        self.chooseMaterialBox.clear()
        self.chooseMaterialBox.addItems(boto3Simulation.materialTypes[test])
        if(test == "Tensile"):
            self.exportButton.setEnabled(True)
        else:
            self.exportButton.setEnabled(False)

    #trigger the export data
    def export_data(self, s):
        try:
            exportData.export(material, test)
            self.successLabel.setText("Success")
            self.successLabel.setStyleSheet("color:lime")
        except FileNotFoundError:
            self.successLabel.setText("Data file not found")
            self.successLabel.setStyleSheet("color:red")
        except TypeError:
            self.successLabel.setText("Data file not found")
            self.successLabel.setStyleSheet("color:red")
        except PermissionError:
            self.successLabel.setText("Permission not given")
            self.successLabel.setStyleSheet("color:red")
    
    #if the dial value has changed
    def modifyDial(self, num):
        self.dialRoll.setValue(num)       

#set up app
app = QApplication(sys.argv)
window = MainWindow()
window.show()

#trigger app
app.exec()

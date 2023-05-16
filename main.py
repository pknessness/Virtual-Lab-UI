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
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

#import localSimulation, 
import boto3Simulation, exportData

conversions = ["HV", "HK", "HB", "HRA", "HRB", "HRC", "HLD", "UT"]

useAWS = True

fps = 30
material = "Aluminum6061"
test = "Tensile"
allFrames = False
#resolution = "720p"

leftIndex = 0
rightIndex = 0
leftNumber = 0
rightNumber = 0

whichIsOut = 0
autoChange = False

def changeConversion(m):
    global leftNumber, rightNumber, rightIndex, leftIndex
    
    if(whichIsOut == 0):
        m.conversionRow[1].setText("")
        m.conversionRow[2].setText("")
        return
    
    hb = 0
    out = 0
    
    inForm = ""
    outForm = ""
    inNum = 0
    
    if(whichIsOut == 1):
        outForm = conversions[leftIndex]
        inForm = conversions[rightIndex]
        inNum = rightNumber
    elif(whichIsOut == 2):
        inForm = conversions[leftIndex]
        outForm = conversions[rightIndex]
        inNum = leftNumber
    
    print(f"num:[{inNum}] from in:[{inForm}] to out:[{outForm}]")
    
    if(inForm == outForm):
        m.conversionRow[whichIsOut].setText(str(inNum))
        return
    
    #E-0([0-9]) ->  * 10**-$1 * 
    
    if(inForm == "HRB"):
        hb = 599 + -34.7* inNum + 0.818*inNum**2 + -8.15 * 10**-3 *inNum**3 + 3.07 * 10**-5 *inNum**4
    elif(inForm == "HRC"):
        hb = 157 + 0.833*inNum + 0.109*inNum**2 + 9.51 * 10**-5 *inNum**3 + -7.96 * 10**-7 *inNum**4
    elif(inForm == "HV"):
        hb = -21.2 + 1.21*inNum + -4.57 * 10**-4 *inNum**2 + -1.63 * 10**-7 *inNum**3 + 1.32 * 10**-10 * inNum**4
    elif(inForm == "HLD"):
        hb = 275 + -2.29*inNum + 7.89 * 10**-3 *inNum**2 + -9.64 * 10**-6 *inNum**3 + 5.11 * 10**-9 *inNum**4
    elif(inForm == "HB"):
        hb = inNum
    print(f"hb {hb}")
    if(outForm == "HRB"):
        out = -46.1 + 1.55 * hb + -6.26 * 10**-3 * hb**2 + 1.18* 10**-5 * hb**3 + -8.34* 10**-9 * hb**4
    elif(outForm == "HRC"):
        out = -80.3 + 0.801 * hb + -2.1 * 10**-3 * hb**2 + 2.68* 10**-6 * hb**3 + -1.27* 10**-9 * hb**4
    elif(outForm == "HV"):
        out = 10 + 0.922 * hb + 1.03 * 10**-4 * hb**2 + -2.33* 10**-7 * hb**3 + 1.51* 10**-9 * hb**4
    elif(outForm == "HLD"):
        out = 139 + 2.37 * hb + -4.19 * 10**-3 * hb**2 + 4.61* 10**-6 * hb**3 + -2.1* 10**-9 * hb**4
    elif(outForm == "HB"):
        out = hb
                
    print(f"out {out}")
    
    m.conversionRow[whichIsOut].setText("{:.1f}".format(out))

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
        
        conversionLayout = QHBoxLayout()
        
        leftForm = QComboBox()
        leftNum = QLineEdit()
        rightNum = QLineEdit()
        rightForm = QComboBox()
        # print(leftForm.size)
        leftForm.resize(200,50)
        self.conversionRow = [leftForm,leftNum,rightNum,rightForm]
        
        leftForm.addItems(conversions)
        rightForm.addItems(conversions)
        
        for i in self.conversionRow:
            conversionLayout.addWidget(i)

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
        
        leftForm.currentIndexChanged.connect(self.leftFormChanged)
        rightForm.currentIndexChanged.connect(self.rightFormChanged)
        leftNum.textChanged.connect(self.leftNumChanged)
        rightNum.textChanged.connect(self.rightNumChanged)

        for w in widgets:
            layout.addWidget(w)

        layout.addLayout(conversionLayout)

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
            
        if(test.find("Hardness") != -1):
            for i in self.conversionRow:
                i.setEnabled(True)
        else:
            for i in self.conversionRow:
                i.setEnabled(False)

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
        except:
            self.successLabel.setText("Undefined Error")
            self.successLabel.setStyleSheet("color:red")
    
    #if the dial value has changed
    def modifyDial(self, num):
        self.dialRoll.setValue(num)       

    def leftFormChanged(self, ind):
        global leftIndex, autoChange
        if(autoChange == False):
            leftIndex = ind
            autoChange = True
            changeConversion(self)
            autoChange = False
    
    def rightFormChanged(self, ind):
        global rightIndex, autoChange
        if(autoChange == False):
            rightIndex = ind
            autoChange = True
            changeConversion(self)
            autoChange = False
        
    def leftNumChanged(self, num):
        global leftNumber, whichIsOut, autoChange
        if(autoChange == False):
            if(num == ""):
                whichIsOut = 0
            else:
                try:
                    leftNumber = float(num)
                except ValueError:
                    self.conversionRow[1].setText(str(leftNumber))
            whichIsOut = 2
            autoChange = True
            changeConversion(self)
            autoChange = False
    
    def rightNumChanged(self, num):
        global rightNumber, whichIsOut, autoChange
        if(autoChange == False):
            if(num == ""):
                whichIsOut = 0
            else:
                try:
                    rightNumber = float(num)
                except ValueError:
                    self.conversionRow[2].setText(str(rightNumber))
            whichIsOut = 1
            autoChange = True
            changeConversion(self)
            autoChange = False
        
        
        

#set up app
app = QApplication(sys.argv)
window = MainWindow()
window.show()

#trigger app
app.exec()

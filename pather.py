import boto3, cv2, pygame, globals, pygame_widgets, sys
from pygame_widgets.slider import Slider
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
import PyQt5

print('Path to module:',cv2.__file__)
print('Path to module:',boto3.__file__)
print('Path to module:',pygame.__file__)
print('Path to module:',pygame_widgets.__file__)
#print('Path to module:',sys.__file__)
print('Path to module:',PyQt5.__file__)
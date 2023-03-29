import pygame, cv2, time
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
    #appSlider = QApplication(sys.argv)
    sliderbar = TimeScale()
    sliderbar.show()

    #appSlider.exec()  

videoBaseDirectory = "videos/"
dataBaseDirectory = "raw_data/"

def runWindow(fps, material, test, trueTimeFlag):

    videoDirectory = videoBaseDirectory+test+"/"+material+"Full.mp4"

    video = cv2.VideoCapture(videoDirectory)
    video.set(cv2.CAP_PROP_FPS, fps)
    #video.set(cv2.CAP_PROP_POS_FRAMES, 300)

    success, video_image = video.read()

    if(not success):
        raise FileNotFoundError(videoDirectory, "not found")

    window = pygame.display.set_mode((600,400), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    print('Path to module:',pygame.__file__)

    run = success

    pygame.init()
    
    time = 0

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        success, video_image = video.read()

        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
            #print(f"size: {len(video_image.tobytes())}, dims: {video_image.shape[1::-1]}")
            print(f"frame 1: {video_image.tobytes()[0]}|{video_image.tobytes()[5]}|{video_image.tobytes()[1249]}|{video_image.tobytes()[100000]}|{video_image.tobytes()[12502]}")
        else:
            #run = False
            continue

        window.blit(pygame.transform.scale(video_surf,scaledSize(pygame.display.get_surface().get_size(), video_surf.get_size())), (0, 0))
        pygame.display.flip()

        time += clock.get_time()
        #print(time, ", ", trueTimeFlag)
        if(trueTimeFlag):
            video.set(cv2.CAP_PROP_POS_FRAMES, int(time * fps / (1000.0)))

    pygame.quit()
    #exit()

def scaledSize(screen, surf):
    scale = screen[0]/surf[0]
    if(surf[1] * scale > screen[1]):
        scale = screen[1]/surf[1] 

    return (int(surf[0] * scale), int(surf[1] * scale))
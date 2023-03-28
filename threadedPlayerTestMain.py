# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

import pygame

videoDirectory = "videos/"
dataDirectory = "raw_data/"


videoDIR = r"C:\Users\ansha\Videos\Captures\yuzu 1252 _ Mario Party Superstars (64-bit) _ 1.0.0 _ NVIDIA 2022-11-26 23-24-46.mp4"
video2DIR = "videos/Hardness/Brass360Full.mp4"

fvs = FileVideoStream(videoDIR).start()
fvs2 = FileVideoStream(video2DIR).start()

# start the FPS timer
fps = FPS().start()

def scaledSize(screen, surf):
    scale = screen[0]/surf[0]
    if(surf[1] * scale > screen[1]):
        scale = screen[1]/surf[1] 

    return (int(surf[0] * scale), int(surf[1] * scale))

if(not fvs.more()):
    raise FileNotFoundError(videoDIR, "not found")
elif(not fvs2.more()):
    raise FileNotFoundError(video2DIR, "not found")
#fps = video.get(cv2.CAP_PROP_FPS)

window = pygame.display.set_mode((1280, 720), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()

print('Path to module:',pygame.__file__)

run = fvs.more() and fvs2.more()

#print(f"fps {fps}")

pygame.init()
while run:
    clock.tick(300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #success, video_image = video.read()
    video2_image = fvs2.read()
    # if success:
    #     video_surf = pygame.image.frombuffer(
    #         video_image.tobytes(), video_image.shape[1::-1], "BGR")
    # else:
    #     run = False

    if fvs2.more():
        video2_surf = pygame.image.frombuffer(
            video2_image.tobytes(), video2_image.shape[1::-1], "BGR")
    else:
        run = False

    #window.blit(pygame.transform.scale(video_surf,(640,400)), (800, 150))
    window.blit(pygame.transform.scale(video2_surf,scaledSize(pygame.display.get_surface().get_size(), video2_surf.get_size())), (0, 0))
    pygame.display.flip()

pygame.quit()
#exit()
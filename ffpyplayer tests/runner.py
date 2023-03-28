from ffpyplayer.player import MediaPlayer
import ffpyplayer
import numpy as np
import pygame
import cv2
import time
from PIL import Image
from io import StringIO
import os

flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE
width = 0
height = 0  # fullscreeen

#screen = pygame.display.set_mode( ( width, height ), flags )

player = MediaPlayer("videosmallest.mp4")
val = ''
while val != 'eof':
    frame, val = player.get_frame()
    if val != 'eof' and frame is not None:
        img, t = frame
        w = img.get_size()[0] 
        h = img.get_size()[1]
        ray = img.to_bytearray()[0];
        #for x in img.to
        #image = pygame.image.load(img)
        #print(ray)
        #im = Image.open(StringIO(ray))
        #im.show()
        #mem = img.to_memoryview()[0]
        #image = pygame.image.frombuffer(img.to_memoryview()[0], ( w, h ), 'BGR')

        bgrImage = np.array( ray).reshape(h, w, 3)
        cv2.imshow('a', bgrImage)

        # copy data on screen at position (0, 0)
        #screen.blit(image, ( 0, 0 ))
        # arr = np.uint8(np.asarray(list(img.to_bytearray()[0])).reshape(h,w,3)) # h - height of frame, w - width of frame, 3 - number of channels in frame
        # cv2.imshow('test', arr)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        # display img

import numpy as np

from viewer import Viewer

def update():
    image = np.random.random((600, 600, 3)) * 255.0
    image[:,:200,0] = 255.0
    image[:,200:400,1] = 255.0
    image[:,400:,2] = 255.0
    return image.astype('uint8')

viewer = Viewer(update, (600, 600))
viewer.start()
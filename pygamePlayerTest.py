import pygame
import moviepy.editor

pygame.init()
video = moviepy.editor.VideoFileClip("vido.mp4")
video.preview()
pygame.quit()
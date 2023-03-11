import pygame
import cv2

def runWindow():

    video = cv2.VideoCapture(r"C:\Users\ansha\Videos\Captures\yuzu 1252 _ Mario Party Superstars (64-bit) _ 1.0.0 _ NVIDIA 2022-11-26 23-24-46.mp4")
    video2 = cv2.VideoCapture("video.mp4")

    success, video_image = video.read()
    success2, video2_image = video2.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    window = pygame.display.set_mode(video_image.shape[1::-1])
    window2 = pygame.display.set_mode((500,500))
    clock = pygame.time.Clock()

    print('Path to module:',pygame.__file__)

    run = success

    pygame.init()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        success, video_image = video.read()
        success2, video2_image = video2.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False

        if success:
            video2_surf = pygame.image.frombuffer(
                video2_image.tobytes(), video2_image.shape[1::-1], "BGR")
        else:
            run = False

        window.blit(pygame.transform.scale(video_surf,(640,400)), (200, 150))
        window.blit(pygame.transform.scale(video2_surf,(640,400)), (800, 200))
        pygame.display.flip()

    pygame.quit()
    #exit()
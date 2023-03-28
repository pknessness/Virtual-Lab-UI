import pygame
import cv2

videoDirectory = "videos/"
dataDirectory = "raw_data/"

def runWindow(fps, material, test):

    videoDIR = r"C:\Users\ansha\Videos\Captures\yuzu 1252 _ Mario Party Superstars (64-bit) _ 1.0.0 _ NVIDIA 2022-11-26 23-24-46.mp4"
    video2DIR = "videos/"+test+"/"+material+"Full.mp4"

    video = cv2.VideoCapture(videoDIR)
    video2 = cv2.VideoCapture(video2DIR)
    video2.set(cv2.CAP_PROP_FPS, fps)

    success, video_image = video.read()
    success2, video2_image = video2.read()

    if(not success):
        raise FileNotFoundError(videoDIR, "not found")
    elif(not success2):
        raise FileNotFoundError(video2DIR, "not found")
    #fps = video.get(cv2.CAP_PROP_FPS)

    window = pygame.display.set_mode(video_image.shape[1::-1], pygame.RESIZABLE)
    clock = pygame.time.Clock()

    print('Path to module:',pygame.__file__)

    run = success

    #print(f"fps {fps}")

    pygame.init()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #success, video_image = video.read()
        success2, video2_image = video2.read()
        # if success:
        #     video_surf = pygame.image.frombuffer(
        #         video_image.tobytes(), video_image.shape[1::-1], "BGR")
        # else:
        #     run = False

        

        if success2:
            video2_surf = pygame.image.frombuffer(
                video2_image.tobytes(), video2_image.shape[1::-1], "BGR")
        else:
            run = False

        #window.blit(pygame.transform.scale(video_surf,(640,400)), (800, 150))
        window.blit(pygame.transform.scale(video2_surf,scaledSize(pygame.display.get_surface().get_size(), video2_surf.get_size())), (0, 0))
        pygame.display.flip()

    pygame.quit()
    #exit()

def scaledSize(screen, surf):
    scale = screen[0]/surf[0]
    if(surf[1] * scale > screen[1]):
        scale = screen[1]/surf[1] 

    return (int(surf[0] * scale), int(surf[1] * scale))
import boto3, cv2, pygame, globals, pygame_widgets, sys
from pygame_widgets.slider import Slider

from credentials import ACCESS_KEY, SECRET_KEY

s3_client = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    #aws_session_token=SESSION_TOKEN
    )
        
videoBaseDirectory = "videos/"
dataBaseDirectory = "raw_data/"

def runWindow(fps, material, test, trueTimeFlag):
    frameCount = 0    
    
    frames = []
    key = videoBaseDirectory + test + "/" + material + "Full.mp4"

    #print(f"key: {key}")                

    url = s3_client.generate_presigned_url('get_object', 
                                        Params = {'Bucket': "vlabtesting", 'Key': key}, 
                                        ExpiresIn = 2400) #this url will be available for 600 seconds
        
    print(f"url: {url}")
    cap = cv2.VideoCapture(url)
        
    ret, frame = cap.read() 

    video = cv2.VideoCapture(url)
    video.set(cv2.CAP_PROP_FPS, fps)
    frameMax = video.get(cv2.CAP_PROP_FRAME_COUNT)
    #video.set(cv2.CAP_PROP_POS_FRAMES, 300)

    success, video_image = video.read()

    if(not success):
        raise FileNotFoundError(url, "not found")

    window = pygame.display.set_mode((600,400), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    print('Path to module:',pygame.__file__)
    print('Path to module:',pygame_widgets.__file__)

    run = success

    pygame.init()
    slider = Slider(window, 0, pygame.display.get_window_size()[1] - 30, pygame.display.get_window_size()[0], 30, curved = False, handleRadius = 15, max = frameMax, color = (60,60,60))

    time = 0
    prevSelect = False

    while run:
        clock.tick(fps)
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.VIDEORESIZE:
                val = slider.getValue()
                slider = Slider(window, 0, pygame.display.get_window_size()[1] - 30, pygame.display.get_window_size()[0], 30, curved = False, handleRadius = 15, max = frameMax, color = (60,60,60), value = val)

        slider.listen(events)
        if((not slider.selected) and (not prevSelect)):
            frameNumber = video.get(cv2.CAP_PROP_POS_FRAMES)
            slider.setValue(frameNumber)
        
        if((not slider.selected) and prevSelect):
            video.set(cv2.CAP_PROP_POS_FRAMES, slider.getValue())
        
        success, video_image = video.read()

        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
            continue

        window.blit(pygame.transform.scale(video_surf,scaledSize(pygame.display.get_surface().get_size(), video_surf.get_size())), (0, 0))
        #slider.y = pygame.display.get_window_size()[1] - 30
        #slider.width = pygame.display.get_window_size()[0]
        slider.draw()
        
        pygame.display.flip()

        time += clock.get_time()
        if(globals.manualModify):
            video.set(cv2.CAP_PROP_POS_FRAMES, globals.getFrame())
            globals.manualModify = False
        else:
            globals.mod(video.get(cv2.CAP_PROP_POS_FRAMES))
        if(globals.getSlider() != None):
            print(f"fnum{globals.getFrame()}")
            globals.getSlider().modify(globals.getFrame())
        
        prevSelect = slider.selected
        
    window = pygame.display.set_mode((600,400))
    standby = pygame.image.load('standby.png')
    window.blit(standby, (0,0))
    pygame.display.flip()
#exit()

def scaledSize(screen, surf):
    scale = screen[0]/surf[0]
    if(surf[1] * scale > screen[1]):
        scale = screen[1]/surf[1] 

    return (int(surf[0] * scale), int(surf[1] * scale))
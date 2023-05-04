import boto3, cv2, pygame, pygame_widgets, sys, pysrt
from datetime import time, datetime
from pygame_widgets.slider import Slider

from credentials import ACCESS_KEY, SECRET_KEY

s3_client = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    #aws_session_token=SESSION_TOKEN
    )      
       
#constants 
bucket = "vlabtesting"

videoBaseDirectory = "videos/"

testTypes = []
materialTypes = {"":[]}

barColor = (200,200,200)
handleWidth = 10
handleHeight = 35
sliderHeight = 30
resolution = "default"

sliderOn = False

#indexing video files 
result = s3_client.list_objects(Bucket=bucket, Prefix=videoBaseDirectory, Delimiter='/')
for o in result.get('CommonPrefixes'):

    #indexing test types
    t = o.get('Prefix').split("/")[1]
    
    if(t == "Hardness"):
        t = "RockwellHardness"
        
    t2 = t[0]
    for i in t[1:]:
        if(i.isupper()):
            t2 = t2 + " " + i
        else:
            t2 = t2 + i
            
    materialDir = o.get('Prefix')

    mats = s3_client.list_objects(Bucket=bucket, Prefix=materialDir, Delimiter='/')

    #indexing material types
    materialTypes[t] = []
    for jo in mats.get('Contents'):
        
        fullKey = jo.get('Key').split("/")
        mat = fullKey[len(fullKey)-1]
        
        if(len(mat) == 0):
            continue
        
        mat = mat.replace("Full","").replace(".mp4","").replace(".mov","")
        #mat2 = mat[0]
        mat2 = ""
        prevSpace = True
        
        for j in mat:
            if(j.isupper() and not prevSpace):
                mat2 = mat2 + " " + j
            elif(j.isnumeric() and not prevSpace):
                mat2 = mat2 + " " + j
            else:
                mat2 = mat2 + j
                prevSpace = False
            if(j.isupper() or j.isnumeric()):
                prevSpace = True
        if(not t2 in materialTypes):
            materialTypes[t] = [mat2]
        else:
            materialTypes[t].append(mat2)
            
    testTypes.append(t2)
    
print(materialTypes)

def runWindow(fps, material, test, trueTimeFlag):
    subs = pysrt.open('subs.srt')
    subIndex = 0
    frameCount = 0
    
    frames = []
    key = ""
    if(resolution == "4K" or resolution == "default"):
        key = videoBaseDirectory + test + "/" + material + "Full.mp4"
    else:
        key = videoBaseDirectory + test + "/" + material + "Full"+ resolution +".mp4"             
    
    url = s3_client.generate_presigned_url('get_object', 
                                        Params = {'Bucket': bucket, 'Key': key}, 
                                        ExpiresIn = 2400) #this url will be available for 40 minutes
        
    print(f"Temporary URL: {url}")
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
    if(sliderOn):
        slider = Slider(window, 0, pygame.display.get_window_size()[1] - sliderHeight, pygame.display.get_window_size()[0], sliderHeight, curved = False, handleRadius = 15, max = frameMax, color = barColor, handleColor = barColor)

    font = pygame.font.Font('freesansbold.ttf', 32) 

    prevSelect = False
    paused = False
    prevFrame = 0
    setFrame = True

    onClickPos = (0,0)
    offClickPos = (0,0)
    holdPos = (0,0)
    mousePrevPress = False
    zoomed = False

    while run:
        clock.tick(fps)
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.VIDEORESIZE:
                if(sliderOn):
                    val = slider.getValue()
                    slider = Slider(window, 0, pygame.display.get_window_size()[1] - sliderHeight, pygame.display.get_window_size()[0], sliderHeight, curved = False, handleRadius = 15, max = frameMax, color = (0,0,0), handleColor = (0,0,0), value = val)
            elif (pygame.mouse.get_pressed()[0] and not mousePrevPress):
                onClickPos = pygame.mouse.get_pos()
                holdPos = pygame.mouse.get_pos()
            elif (not pygame.mouse.get_pressed()[0] and mousePrevPress):
                offClickPos = pygame.mouse.get_pos()
                if(onClickPos[0] != offClickPos[0] and onClickPos[1] != offClickPos[1]):
                    zoomed = True
            elif (pygame.mouse.get_pressed()[0]):
                holdPos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                zoomed = False
                #pygame.quit()
            # elif (not pygame.mouse.get_pressed()[0]):
            #     holdPos = (0,0)
        mousePrevPress = pygame.mouse.get_pressed()[0]
                
        if(sliderOn):
            slider.listen(events)
        
        
        
            if((not slider.selected) and prevSelect):
                paused = False
                video.set(cv2.CAP_PROP_POS_FRAMES, slider.getValue())
            
        frameNumber = video.get(cv2.CAP_PROP_POS_FRAMES)
        locX = int(pygame.display.get_window_size()[0] * float(frameNumber)/frameMax)
        
        if(sliderOn):
            pygame.draw.rect(window,(0,0,0), (0, pygame.display.get_window_size()[1] - handleHeight, pygame.display.get_window_size()[0], handleHeight))
            
            if((not slider.selected) and (not prevSelect)):
                slider.setValue(frameNumber)
                #pygame.draw.rect(window,(240,100,90), (0, pygame.display.get_window_size()[1] - sliderHeight, locX, sliderHeight))
                #r.update()
        
            if(slider.selected ):
                pygame.draw.rect(window,barColor, (0, pygame.display.get_window_size()[1] - sliderHeight, pygame.display.get_window_size()[0], sliderHeight))
                pygame.draw.rect(window,(240,100,90), (0, pygame.display.get_window_size()[1] - sliderHeight, locX, sliderHeight))
                pygame.draw.rect(window,(254,10,10), (int(pygame.display.get_window_size()[0] * float(slider.getValue())/frameMax) - handleWidth/2, pygame.display.get_window_size()[1] - handleHeight, handleWidth, handleHeight))
                
                pygame.display.update((0, pygame.display.get_window_size()[1] - handleHeight, pygame.display.get_window_size()[0], handleHeight))
                #pygame.display.flip()
        
        
        success, video_image
        if(paused):
            success = True
            video_image = prevFrame
        else:
            success, video_image = video.read()
            prevFrame = video_image
            # if(setFrame == False):
            #     prevFrame = video_image
            #     setFrame = True
            
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
            continue


        if(sliderOn):
            slider.handleColour = (barColor)
            if(not slider.selected):
                slider.draw()

        boxSize = (abs(onClickPos[0]-offClickPos[0]),abs(onClickPos[1]-offClickPos[1]))
        if(boxSize[0] <= 20 or boxSize[1] <= 20):
            zoomed = False
            
        if(not zoomed):
            window.blit(pygame.transform.scale(video_surf,scaledSize(pygame.display.get_surface().get_size(), video_surf.get_size())), (0, 0))
        else:
            # virtualSize = (pygame.display.get_window_size()[0] * video_surf.get_size()[0] / boxSize[0],pygame.display.get_window_size()[1] * video_surf.get_size()[1] / boxSize[1])
            virtualDisplacement = (-pygame.display.get_window_size()[0] / video_surf.get_size()[0] * onClickPos[0],-pygame.display.get_window_size()[1] / video_surf.get_size()[1] * onClickPos[1])
            # window.blit(pygame.transform.scale(video_surf,scaledSize(virtualSize, video_surf.get_size())), virtualDisplacement)
            print(f"boxSize:{boxSize} vDisp: {virtualDisplacement}")
            window.blit(pygame.transform.scale(video_surf,scaledSize(pygame.display.get_surface().get_size(), video_surf.get_size())), (0, 0, boxSize[0],boxSize[1]))
            
        if(sliderOn):
            topLeft = (min(onClickPos[0],holdPos[0]),min(onClickPos[1],holdPos[1]))
            pygame.draw.rect(window, (10,200,20), (topLeft[0],topLeft[1],abs(onClickPos[0] - holdPos[0]),abs(onClickPos[1] - holdPos[1])))
            print(f"onClick:{onClickPos}, hoo:{(onClickPos[0] - holdPos[0],onClickPos[1] - holdPos[1])}")
            
            pygame.draw.rect(window,(240,100,90), (0, pygame.display.get_window_size()[1] - sliderHeight, locX, sliderHeight))
            pygame.draw.rect(window,(254,10,10), (locX - handleWidth/2, pygame.display.get_window_size()[1] - handleHeight, handleWidth, handleHeight))
        
        font = pygame.font.Font('freesansbold.ttf', int(pygame.display.get_window_size()[1]/32)) 
        #print(type(subs[subIndex].end.to_time()))
        if(len(subs) > subIndex):
            print(subs[subIndex].end.to_time())
            
            tex = subs[subIndex]
            text = font.render(subs[subIndex].text, True, (250,250,250), (0,0,0,100))
            textRect = text.get_rect()
    
            # set the center of the rectangular object.
            textRect.center = (pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] * 0.9)
            window.blit(text, textRect)
            if(subs[subIndex].end.to_time() < time(hour=int(frameNumber / (fps * 360))%24,minute=int(frameNumber / (fps * 60))%60,second=int(frameNumber / fps)%60,microsecond=int(1000000 * frameNumber / fps)%1000000)):
                print("next")
                subIndex+=1
            #if(len(subs) <= subIndex):
                pygame.draw.rect(window,(0,0,0),textRect)
        pygame.display.flip()

        if(sliderOn):
            prevSelect = slider.selected
        if(frameNumber == frameMax - 1):
            paused = True
            
        
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
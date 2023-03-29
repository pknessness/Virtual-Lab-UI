import boto3
import pygame, cv2
import moviepy.editor

ACCESS_KEY = "AKIAUG6FEDU36WL6CGYX"
SECRET_KEY = "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"

s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    #aws_session_token=SESSION_TOKEN
    )
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket}')

resource = boto3.resource('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    #aws_session_token=SESSION_TOKEN
    )
vlab = resource.Bucket('vlabtesting')

vid = 0
for obj in vlab.objects.all():
    print(f"obj: {obj}")
    body = obj.get()
    print(body)
    vid = obj
    break

#video = cv2.VideoCapture(obj.get()['Body'])
#success, video_image = video.read()
#fps = video.get(cv2.CAP_PROP_FPS)
fps = 30

window = pygame.display.set_mode((1080,1920), pygame.RESIZABLE)
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #success, video_image = video.read()
    frame = vid.get()['Body'].read(6220800)
    if True:
        video_surf = pygame.image.frombuffer(
            frame, (1080,1920), "BGR")
        print(f"frame 1: {frame[0]}|{frame[5]}|{frame[1249]}|{frame[100000]}|{frame[12502]}")
    else:
        run = False
    window.blit(video_surf, (0, 0))
    pygame.display.flip()

pygame.quit()
exit()
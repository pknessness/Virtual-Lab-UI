frameNum = 0
frameMax = 30
slider = None
manualModify = False
autoModify = False

def mod(f):
    global frameNum
    frameNum = f
    print(f"set - frameNum:[{frameNum}]")

def getFrame():
    #print(f"get - frameNum:[{frameNum}]")
    return frameNum

def setSlider(slid):
    global slider
    slider = slid

def getSlider():
    return slider
    

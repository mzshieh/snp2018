import sys

cnt = 0
buf = []

def get_input():
    try:
        tbuf = input().split()
    except:
        raise Exception("No inputs")

    buf.extend(tbuf)
    global cnt
    cnt += len(tbuf)

    if len(tbuf)==0:
        get_input()
        

def get_str():
    global cnt
    if cnt==0:
        try:
            get_input()
        except:
            print("Error: No inputs")
            sys.exit()
            
    s = buf[0]
    buf.pop(0)
    cnt-=1
    return s

def get_int():
    while True:
        try:
            i = int( get_str() )
        except ValueError:
            print("Not int. Please try again")
            continue
        except :
            sys.exit()
        return i

def get_float():
    while True:
        try:
            f = float( get_str() )
        except ValueError:
            print("Not float. Please try again")
            continue
        except :
            sys.exit()
        return f
    
from mss import mss
from PIL import Image
import cv2 as cv
import numpy as np

def screenshot(region=None, **kwargs):
    im = None
    monitors = None
    if region == None:
        region = kwargs.get('region')
    
    with mss() as sct:

        # Region to capture
        monitor = sct.monitors[1]
        if region != None:
            monitor['left'] = int(region[0])
            monitor['top'] = int(region[1])
            monitor['width'] = int(region[2])
            monitor['height'] = int(region[3])

        # Get pixels on image
        sct_img = sct.grab(monitor)
        im = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
        im = im.convert('RGB')
    return im

def locateOnScreen(dino, threshold=0.87, region=(0,0,600,200)):
    if type(dino) is not np.ndarray :
        dino = cv.imread(dino,cv.IMREAD_COLOR) # BGR Color
    
    result = screenshot(dino,region)
    _minVal, maxVal, _minLoc, maxLoc = cv.minMaxLoc(result, None)
    
    if maxVal >= threshold:
        return ( maxLoc[0]+region[0], maxLoc[1]+region[1], dino.shape[0], dino.shape[1] )
    else:
        return None

def locateCenterOnScreen(dino, threshold=0.87, region=(0,0,600,200)):
    p = locateOnScreen(dino,threshold,region)
    if p != None:
        p = ( p[0]+p[2]//2, p[1]+p[3]//2 )
    return p

def locateAllOnScreen(dino, threshold=0.87, region=(0,0,600,200)):
    if type(dino) is not np.ndarray :
        dino = cv.imread(dino,cv.IMREAD_COLOR) # BGR Color
    
    result = screenshot(dino,region)
    loc = np.where( result >= threshold )
    
    for pt in zip(*loc[::-1]):
        yield( (region[0]+pt[0], region[1]+pt[1], dino.shape[0], dino.shape[1]) )

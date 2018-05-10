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
from pyautogui import size

def screenshot(dino, region):
    bbox={'left': region[0], 'top': region[1], 'width': region[2], 'height': region[3]} # detect box
    
    with mss() as sct:
        mss_im = sct.grab(bbox)
    im = np.array(mss_im.pixels,np.uint8)
    im = cv.cvtColor(im, cv.COLOR_RGB2BGR)
    cv.imshow('bbox', im)
    result = cv.matchTemplate(im, dino, cv.TM_CCOEFF_NORMED)
    return result

def locateOnScreen(dino, threshold=0.87, region=None):
    if region == None: region = (0,0)+size()
    if type(dino) is not np.ndarray :
        dino = cv.imread(dino,cv.IMREAD_COLOR) # BGR Color
    
    result = screenshot(dino,region)
    _minVal, maxVal, _minLoc, maxLoc = cv.minMaxLoc(result, None)
    
    if maxVal >= threshold:
        return ( maxLoc[0]+region[0], maxLoc[1]+region[1], dino.shape[0], dino.shape[1] )
    else:
        return None

def locateCenterOnScreen(dino, threshold=0.87, region=None):
    if region == None: region = (0,0)+size()
    p = locateOnScreen(dino,threshold,region)
    if p != None:
        p = ( p[0]+p[2]//2, p[1]+p[3]//2 )
    return p

def locateAllOnScreen(dino, threshold=0.87, region=None):
    if region == None: region = (0,0)+size()
    if type(dino) is not np.ndarray :
        dino = cv.imread(dino,cv.IMREAD_COLOR) # BGR Color
    
    result = screenshot(dino,region)
    loc = np.where( result >= threshold )
    
    for pt in zip(*loc[::-1]):
        yield( (region[0]+pt[0], region[1]+pt[1], dino.shape[0], dino.shape[1]) )

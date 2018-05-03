# reference: https://docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html

from mss import mss
import cv2 as cv
import numpy as np
from time import time
from pyautogui import position, size
 
dino = cv.imread('dino.png',cv.IMREAD_COLOR) # BGR Color
frames = 0 # record frame number
bbox={'left': 340, 'top': 114, 'width': 600, 'height': 200} # detect box
begin = time() # start time
while True:
    bbox['left'], bbox['top'] = position()  
    bbox['left'] = min(size()[0]-bbox['width']-1,bbox['left'])
    bbox['top'] = min(size()[1]-bbox['height']-1,bbox['top'])
    with mss() as sct:
        mss_im = sct.grab(bbox)
    im = np.array(mss_im.pixels,np.uint8)
    
    # print(im.shape) => (400, 1200, 3)
    
    im = cv.cvtColor(im, cv.COLOR_RGB2BGR) # Convert screenshot from RGB to BGR
    result = cv.matchTemplate(im, dino, cv.TM_CCOEFF_NORMED) # TM_CCOEFF return the maximum 
    _minVal, maxVal, _minLoc, maxLoc = cv.minMaxLoc(result, None)
    print('#', maxLoc, maxVal)

    # Multiple matching
    threshold = 0.7
    loc = np.where( result >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(im, pt, (pt[0] + dino.shape[0], pt[1] + dino.shape[1]), (0,255,0), 2)
        print('->', pt, result[pt[::-1]])
    # end Multiple matching
    
    cv.imshow('bbox', im)
    frames += 1 
    if 13 == cv.waitKey(1): # Return key
        break
end = time()
print(frames/(end-begin)) # frame per second
cv.destroyAllWindows()

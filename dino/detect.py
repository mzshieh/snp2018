from mss import mss
import cv2 as cv
import numpy as np
from time import time
from pyautogui import position, size

dino = cv.imread('dino.png',cv.IMREAD_COLOR)
frames = 0
bbox={'left':340, 'top': 114, 'width': 600, 'height': 200}
begin = time()
while True:
    bbox['left'], bbox['top'] = position()
    bbox['left'] = min(size()[0]-bbox['width']-1,bbox['left'])
    bbox['top'] = min(size()[1]-bbox['height']-1,bbox['top'])
    with mss() as sct:
        mss_im = sct.grab(bbox)
    im = np.array(mss_im.pixels,np.uint8)
    im = cv.cvtColor(im, cv.COLOR_RGB2BGR)
    result = cv.matchTemplate(im, dino, cv.TM_CCOEFF)
    cv.normalize( result, result, 0, 1, cv.NORM_MINMAX, -1 )
    _minVal, maxVal, _minLoc, maxLoc = cv.minMaxLoc(result, None)
    print(maxLoc, maxVal)
    cv.rectangle(im, maxLoc, (maxLoc[0] + dino.shape[0], maxLoc[1] + dino.shape[1]), (0,255,0), 2, 8, 0)
    cv.imshow('bbox', im)
    frames += 1
    if 13 == cv.waitKey(1):
        break
end = time()
print(frames/(end-begin))
cv.destroyAllWindows()

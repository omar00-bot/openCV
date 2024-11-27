import cv2 as cv
import numpy as np

map = cv.imread('map.jpg', cv.IMREAD_REDUCED_COLOR_2)
robot = cv.imread('robot.jpg', cv.IMREAD_REDUCED_COLOR_2)

result = cv.matchTemplate(map, robot, cv.TM_CCOEFF_NORMED)

#Get the best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
 
print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

threshold = 0.8
if max_val >= threshold:
    print('Robot found')
    
    needle_w = robot.shape[1]
    needle_h = robot.shape[0]
    
    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
    
    cv.rectangle(map, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
    
    # cv.imshow('result', map)
    # cv.waitKey()
    
    cv.imwrite('result.jpg',map)
else:
    print('Robot not found')

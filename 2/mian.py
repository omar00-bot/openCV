import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


map = cv.imread('map.jpg', cv.IMREAD_REDUCED_COLOR_2)
robot = cv.imread('robot.jpg', cv.IMREAD_REDUCED_COLOR_2)

result = cv.matchTemplate(map, robot, cv.TM_CCOEFF_NORMED)
print(result)

threshold = 0.30 
locations = np.where(result >= threshold) 
locations = list(zip(*locations[::-1])) 
print(locations) 

if locations:
    print('Found needle.')

    needle_w = robot.shape[1]
    needle_h = robot.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        print(top_left)
        print(bottom_right)
        # Draw the box
        cv.rectangle(map, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', map)
    cv.waitKey()
    #cv.imwrite('result.jpg', haystack_img)
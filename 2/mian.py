import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


map = cv.imread('map.jpg', cv.IMREAD_REDUCED_COLOR_2)
robot = cv.imread('robot.jpg', cv.IMREAD_REDUCED_COLOR_2)

result = cv.matchTemplate(map, robot, cv.TM_CCOEFF_NORMED)
print(result)

threshold = 0.70 
locations = np.where(result >= threshold) 
locations = list(zip(*locations[::-1]))
print(locations) 

# locations = list(zip(*locations[::-1]))
# print(locations)
import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
from PIL import ImageGrab
from grab_screen import grab_screen
import win32gui
import win32ui
import win32con



# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('OpenCV: Template Matching - Google Chrome')

loop_time = time()
while(True):
    screenshot = grab_screen(region=(1280, 0, 3840, 1440))

    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    print(screenshot)
    cv.imshow('Computer vision', screenshot)
    
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waitKey(1) will delay for 1ms every loop to process the key press
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
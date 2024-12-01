import cv2 as cv
import os
from time import time
from windowcapture import window_capture



# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))




wincap = window_capture('Welcome to TeraBox')

# captures all the windows opened 
# comment if done on using it
# wincap.list_window_name()

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()
    cv.imshow('Computer vision', screenshot)
    
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waitKey(1) will delay for 1ms every loop to process the key press
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
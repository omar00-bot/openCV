import cv2 as cv
import os
from windowcapture import window_capture
from time import time



# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# captures all the windows opened 
# comment if done on using it
# window_capture.list_window_name(self=None)
# exit()

# initialize the window_capture class
wincap = window_capture('(123) YouTube - Google Chrome')


loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()
    cv.imshow('Computer vision', screenshot)
    
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waitKey(1) will delay for 1ms every loop to process the key press
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
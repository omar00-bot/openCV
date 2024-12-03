import cv2 as cv
import os
from windowcapture import window_capture
from time import time
from vision import Vision



# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# captures all the windows opened 
# comment if done on using it

# window_capture.list_window_name(self=None)
# exit()

# initialize the window_capture class
wincap = window_capture('dBLIND - Flyff Universe - Google Chrome')
# wincap = window_capture('This PC')
find_image = Vision('robot.jpg')

loop_time = time()
while(True):
    # take screnshot of image
    screenshot = wincap.get_screenshot()
    # process the image and show
    find_image.find(screenshot, 0.27, 'rectangles')

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waitKey(1) will delay for 1ms every loop to process the key press
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

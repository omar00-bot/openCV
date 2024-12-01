import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
from PIL import ImageGrab
import win32gui
import win32ui
import win32con

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def window_capture():
    w = 1920 # set this
    h = 1080 # set this
    bmpfilenamename = "out.bmp" #set this

    hwnd = win32gui.FindWindow(None, windowname)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())



loop_time = time()
while(True):
    screenshot = 1

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
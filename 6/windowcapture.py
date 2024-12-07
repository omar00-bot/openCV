import numpy as np
import win32gui, win32ui, win32con
import time

class window_capture:
    
    # properties
    w = 0 
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    window_name = None
    
    # constructor
    def __init__(self, window_name):
        # find the handle of the window we want to capture
        self.window_name = window_name
        if window_name is None:
            print('No window found')
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            print(window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
           

    def get_screenshot(self):
        self.hwnd = win32gui.FindWindow(None, self.window_name)
        Left , Top, Right, Bot = win32gui.GetWindowRect(self.hwnd) 
        self.w = Right - Left
        self.h = Bot - Top
        print(self.w, self.h)
        
        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 8
        self.w = self.w - border_pixels * 2
        self.h = self.h - border_pixels
        self.cropped_x = Left + border_pixels
        self.cropped_y = titlebar_pixels
        # win32gui.SetForegroundWindow(self.hwnd)


        hdesktop = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hdesktop)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x, Top), win32con.SRCCOPY)
        
        # save image
        # dataBitMap.SaveBitmapFile(cDC, 'out.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype=np.uint8)
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)
        
        return img
    
    def list_window_name(self):
    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

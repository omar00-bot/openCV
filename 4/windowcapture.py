import numpy as np
import win32gui, win32ui, win32con

class window_capture:
    
    # properties
    w = 0 
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    
    
    # constructor
    def __init__(self, window_name):
        # find the handle of the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd) 
        self.w = window_rect[2]-window_rect[0]
        self.h = window_rect[3]-window_rect[1]
        
        # # account for the window border and titlebar and cut them off
        # border_pixels = 8
        # titlebar_pixels = 0
        # # self.w = self.w - border_pixels * 2
        # # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels
           

    def get_screenshot(self):
        
        window_rect = win32gui.GetWindowRect(self.hwnd) 
        self.w = window_rect[2]-window_rect[0]
        self.h = window_rect[3]-window_rect[1]
        
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        
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
    
    

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    
    @staticmethod
    def list_window_name():
            def winEnumHandler(hwnd, ctx):
                if win32gui.IsWindowVisible(hwnd):
                    print(hex(hwnd), win32gui.GetWindowText(hwnd))
            win32gui.EnumWindows(winEnumHandler, None)

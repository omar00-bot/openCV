import cv2 as cv
import numpy as np

class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"
    
    # properties
    robot = None
    needle_w = 0
    needle_h = 0
    method = None
    
    # constructor
    def __init__(self, robot_path, method=cv.TM_CCOEFF_NORMED):
        
        self.robot = cv.imread(robot_path, cv.IMREAD_UNCHANGED)  
        self.method = method
        
        self.needle_w = self.robot.shape[1]
        self.needle_h = self.robot.shape[0]
        # print(self.needle_w)
        # print(self.needle_h)
        


    def find(self, screenshot, threshold=0.2):
        result = cv.matchTemplate(screenshot, self.robot, self.method)
        # print(result)

        
        locations = np.where(result >= threshold) 
        locations = list(zip(*locations[::-1])) 
        # print(locations) 

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), int(self.needle_w), int(self.needle_h)]
            rectangles.append(rect)
            rectangles.append(rect)
            # print(rect)


        rectangles , weights = cv.groupRectangles(rectangles, 1, 0.5)
        # print(rectangles)
        
        return rectangles

    def  get_click_points(self, rectangles):
        points = []

        # Loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:             
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            #save the points
            points.append((center_x, center_y))
        
        return points    
            
            
    def draw_rectangles(self, screenshot,  rectangles):
        # these colors are actually BGR
        line_color = (0, 255,0)
        line_type = (cv.LINE_4)
        
        for (x, y, w, h) in rectangles:
            # Determine the box positions
            top_left = (x, y)
            bottom_right = (x+w, y+h)
            # print(top_left)
            # print(bottom_right)
            # Draw the box
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
        
        return screenshot
    
    def draw_crosshair(self, screenshot, points):
        # these colors are actually BGR
        marker_color = (0, 255,0)
        marker_type = (cv.MARKER_CROSS)
        
        for (center_x, center_y) in points:
            # draw the center points
            cv.drawMarker(screenshot, (center_x, center_y), marker_color, marker_type)
            
        return screenshot
    
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)
        
        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass
            
        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
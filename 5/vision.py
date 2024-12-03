import cv2 as cv
import numpy as np

class Vision:
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
        print(self.needle_w)
        print(self.needle_h)
        


    def find(self, screenshot, threshold=0.2, debug_mode=None):
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
            print(rect)


        rectangles , weights = cv.groupRectangles(rectangles, 1, 0.5)
        # print(rectangles)

        points = []
        if len(rectangles):
            print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the locations and draw their rectangle
            for (x, y, w, h) in rectangles:
                
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                #save the points
                points.append((center_x, center_y))
                if debug_mode == 'rectangles':
                # Determine the box positions
                    top_left = (x, y)
                    bottom_right = (x+w, y+h)
                    # print(top_left)
                    # print(bottom_right)
                    # Draw the box
                    cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
                elif debug_mode == 'points':
                    cv.drawMarker(screenshot, (center_x, center_y), marker_color, marker_type)
            
        if debug_mode:  
            cv.namedWindow("Computer vision", cv.WINDOW_NORMAL)      
            screenshot = cv.resize(screenshot, (960, 540)) 
            cv.imshow('Computer vision', screenshot)
        #     cv.imshow('Matches', map)
        #     # cv.waitKey()
        #     #cv.imwrite('result.jpg', haystack_img)
        return points
            
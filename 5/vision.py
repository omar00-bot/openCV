import cv2 as cv
import numpy as np


def findClickPositions(map_path, image_path, threshold=0.2, debug_mode=None):
    # map = cv.imread(map_path, cv.IMREAD_REDUCED_COLOR_2)
    map = map_path
    robot = cv.imread(image_path, cv.IMREAD_UNCHANGED)

    needle_w = robot.shape[1]
    needle_h = robot.shape[0]
    
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(map, robot, method)
    # print(result)

     
    locations = np.where(result >= threshold) 
    locations = list(zip(*locations[::-1])) 
    # print(locations) 

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), int(needle_w), int(needle_h)]
        rectangles.append(rect)
        rectangles.append(rect)


    rectangles , weights = cv.groupRectangles(rectangles, 1, 0.5)
    print(rectangles)

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
                cv.rectangle(map, top_left, bottom_right, line_color, line_type)
            elif debug_mode == 'points':
                cv.drawMarker(map, (center_x, center_y), marker_color, marker_type)
        
    if debug_mode:  
    #     cv.namedWindow("Matches", cv.WINDOW_NORMAL)      
        map = cv.resize(map, (960, 540)) 
        cv.imshow('Computer vision', map)
    #     cv.imshow('Matches', map)
    #     # cv.waitKey()
    #     #cv.imwrite('result.jpg', haystack_img)
    return points
        
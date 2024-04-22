# Authors: Christ Nunez, Ismail Hassan, German Burset Romero

# This program utilizes the OpenCV library and numpy, which OpenCV depends on,
# in order to create a small-scale goal-line detection system of the actual
# system utilized in professional soccer. Image manipulation, mouse recognition,
# color recognition, shape recognition, and camera coordinates were utilized
# in order to check if a ball crosses over the line.

# import opencv and numpy libraries
import cv2
import numpy as np

# setting initial mouse position
mouse_x, mouse_y = -1, -1

# mouse callback function to detect mouse movement across the frame
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

# function which manipulates original camera frame, detects color, and detects a ball
def detect_ball(frame):
    # convert BGR to HSV (original rgb video to hsv to more easily detect ball)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_blue = np.array([110, 50, 50]) 
    upper_blue = np.array([130, 255, 255])

    # make hsv image get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # initialize ball position
    ball_position = None
    
    # check if contours are found and returns the largest one
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # get the minimum diameter that would enclose the largest contour
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        
        # convert float coordinates to integers
        center = (int(x), int(y))
        radius = int(radius)
        top_point = (center[0], center[1] - radius)
        
        # draw circle
        cv2.circle(frame, center, radius, (0, 255, 0), 2)
        
        ball_position = top_point
    
    return ball_position

# initialize video capture
cap = cv2.VideoCapture(2)

cv2.namedWindow('Goal Line System')
cv2.setMouseCallback('Goal Line System', mouse_callback)

line = [(0, 354), (637, 354)]

while True:
    # read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break
    
    ball_position = detect_ball(frame)
    
    cv2.line(frame, line[1], (line[0][0], line[1][1]), (255, 255, 255), 2)

    # if ball is detected, draw a circle around it
    # if ball is past line, change center circle's color
    if ball_position:
        # check if the ball's position is past (below) the line region
        if (ball_position[1] >= line[1][1]):
            # change the color of the circle
            circle_color = (0, 255, 0)  # Green
        else:
            # reset color to red
            circle_color = (0, 0, 255)

        # take a screenshot when ball crosses line (based off circle color)
        if circle_color == (0, 255, 0):
            cv2.imwrite("Goal_Screenshot.png", frame)
            #print("Screenshot saved as Goal_Screenshot.png.")
            cv2.putText(frame, "Goal! Screenshot taken.", (850, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # draw circle
        cv2.circle(frame, ball_position, 10, circle_color, -1)
    
    #display mouse cursor position on the video (can be removed once line won't move)
    #cv2.putText(frame, f"Mouse Position: ({mouse_x}, {mouse_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #cv2.putText(frame, f"Ball Position: {ball_position}", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # display frame
    cv2.imshow('Goal Line System', frame)
    
    # break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video capture
cap.release()
cv2.destroyAllWindows()

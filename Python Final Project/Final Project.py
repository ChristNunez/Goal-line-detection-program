import cv2
import numpy as np

mouse_x, mouse_y = -1, -1

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

def detect_white_ball(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of white color in HSV
    lower_red = np.array([0,10,100])
    upper_red = np.array([10,255,255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize ball position as None
    ball_position = None
    
    # If contours are found
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the minimum enclosing circle
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        
        # Convert float coordinates to integers
        center = (int(x), int(y))
        radius = int(radius)
        
        # Draw the circle
        cv2.circle(frame, center, radius, (0, 255, 0), 2)
        
        ball_position = center
    
    return ball_position

# Initialize video capture
cap = cv2.VideoCapture(1)

cv2.namedWindow('White Ball Tracker')
cv2.setMouseCallback('White Ball Tracker', mouse_callback)

# For me: Change coordinates based off camera!
# [(x1, y1), (x2, y2)] -> [(top right), (bottom left)]
line = [(683, 457), (1052, 534)]

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect white ball
    ball_position = detect_white_ball(frame)
    
    # If ball is detected, draw a circle around it
    if ball_position:
        # Check if the ball's position is within the line region
        if (line[0][0] < ball_position[0] < line[1][0] and
            line[0][1] < ball_position[1] < line[1][1]):
            # Change the color of the circle
            circle_color = (40, 255, 255)  # Yellow
        else:
            # Reset the color to green
            circle_color = (0, 255, 0)
        
        # Draw the circle
        cv2.circle(frame, ball_position, 10, circle_color, -1)
    
    # Display mouse cursor position on the frame
    cv2.putText(frame, f"Mouse Position: ({mouse_x}, {mouse_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('White Ball Tracker', frame)

    #y1 = 457
    #y2 = 534
    #x1 = 683
    #x2 = 1052
    #line = frame[457: 534, 683: 1052]

    #cv2.imshow("line", line)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()
cv2.destroyAllWindows()

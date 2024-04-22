# Goal Line Detection Program
## Authors: German Burset Romero, Ismail Hassan, & Christ Nunez

### This program mimics the VAR Goal Line System utilized in professional soccer. By leveraging the OpenCV and NumPy libraries, my team and I were able to detect when a ball fully crosses the line from a camera above. The ball detection is achieved by converting the frame from BGR to HSV color space and applying a mask to isolate colors depending on what color the ball is. The program continuously captures frames from the video feed, detects the position of the ball, and draws a line representing the goal line. If the ball is detected and its position indicates that it has crossed the goal line, the program takes a screenshot and displays a message indicating a goal has been scored.

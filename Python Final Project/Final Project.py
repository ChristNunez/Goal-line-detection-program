import cv2
import numpy as num


# German Burset Romero, Katerine Gomez, & Christ Nunez
# Final project / CSIT 200-01 Python Programming
# This project is to ...

def main():
#    print("Welcome to OpenCV project")
#    print(cv2.__version__)

    vid = cv2.VideoCapture(0)

    while vid.isOpened():                                   
        ret, frame = vid.read()                         
        width = int(vid.get(3))
        height = int(vid.get(4))

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            vid.release()
            cv2.destroyAllWindows()
            return


if __name__ == '__main__':
    main()

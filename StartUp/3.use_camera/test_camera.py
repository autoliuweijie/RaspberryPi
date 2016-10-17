import numpy as np
import cv2 as cv


def take_photo():
    cap = cv.VideoCapture(0)
    ret, photo = cap.read()
    if ret:
        print "take photo successfuly"
        cv.imwrite("./photo.png", photo)
    else:
        print "Error! Photo failed!"


if __name__ == "__main__":
    take_photo()
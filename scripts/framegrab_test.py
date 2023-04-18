# test script for framegrabbing from a webcam

import cv2
import os

# current working directory
cwd = os.getcwd()

src = int(input("Enter source number: "))
dir = cwd + "\data\\framegrab_test\\"

# open cv2 window
cv2.namedWindow("preview")

# open video capture
vc = cv2.VideoCapture(src)

# try to get the first frame
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    # show the frame
    cv2.imshow("preview", frame)

    # read next frame
    rval, frame = vc.read()

    # wait for keypress or 20ms
    key = cv2.waitKey(20)

    # handle keypress
    if key == 27:  # exit on ESC
        break
    if key == 32:  # write on spacebar
        print("writing frame to " + dir + "frame.png")
        cv2.imwrite(dir + "frame.png", frame)

# close window and video capture
vc.release()
cv2.destroyWindow("preview")

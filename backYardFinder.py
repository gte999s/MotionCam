# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:40:09 2017

@author: pi
"""
import numpy
import datetime
import time

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2

motionCounter = 0
motionCounterMax = 1705    


# capture frames from the camera
for count in range(1705):
    #for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied tex
    frame = cv2.imread("testImages/frame_%d.jpg" % count, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameS = cv2.resize(frame, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
    grayS = cv2.resize(gray, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
    cv2.imshow("Original", frameS)
    cv2.imshow("Gray", grayS)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    key=cv2.waitKey(0)
    print chr(key&255)
    if "q"==chr(key&255):
        break
cv2.destroyAllWindows()    
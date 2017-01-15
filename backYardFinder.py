# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:40:09 2017

@author: pi
"""
import simpleMotionDetector
import shutil
import sys
import os

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2

# cleanup motion capture dir
shutil.rmtree('./motionCaptureImages', ignore_errors=True)
os.makedirs('./motionCaptureImages')

detector=simpleMotionDetector.SimpleMotionDetector(debug=True, thresh_diff=10, avg_ratio=.5)

# capture frames from the camera
for count in range(700-6, 1705):
    # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied tex

    frame = cv2.imread("testImages/frame_%d.jpg" % count, cv2.IMREAD_COLOR)
    frameSmall = cv2.resize(frame,None, fx=.3, fy=.3)

    (isMotion, procFrame) = detector.procFrame(frameSmall)

    if isMotion:
        cv2.imwrite('./motionCaptureImages/HighRes_%d.jpg' % count, frame)
        cv2.imwrite('./motionCaptureImages/LowRes_%d.jpg' % count, procFrame)

    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()

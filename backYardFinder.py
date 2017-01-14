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

fgbg = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=20, detectShadows=True)

motionCounter = 0
motionCounterMax = 1705
avg = None
fgmask = None
text = "Unoccupied"
# capture frames from the camera
for count in range(700-60, 1705):
    # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied tex


    frame = cv2.imread("testImages/frame_%d.jpg" % count, cv2.IMREAD_GRAYSCALE)
    frame = cv2.resize(frame,None,fx=.3,fy=.3)
    #frameBlur=cv2.medianBlur(frame,15)
    frameBlur = cv2.GaussianBlur(frame, (13, 13), 0)
    #frameBlur = frame
    cv2.imshow("Blurred",frameBlur)
    if fgmask is None:
        fgmask=fgbg.apply(frameBlur)
    else:
        fgmask=fgbg.apply(frameBlur,fgmask)



    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    #if text == "Unoccupied":
    #cv2.accumulateWeighted(gray, avg, 0.1)

    text = "Unoccupied"
    #frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    #thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(fgmask, None, iterations=4)
    (junk, cnts, junk2) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    example=thresh
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 1000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(example, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.drawContours(example, [c], 0, (255, 255, 255), 3)

        text = "Occupied"

    frameS = example; #cv2.resize(example, None, fx=.5, fy=.5, interpolation=cv2.INTER_CUBIC)

    frameText="Frame Number: %d" % count
    cv2.putText(frameS, frameText.format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("Frame", frameS)

    if text == "Occupied":
        key = cv2.waitKey(1)
    else:
        key = cv2.waitKey(1)

    #print chr(key & 255)
    if "q" == chr(key & 255):
        break

cv2.destroyAllWindows()

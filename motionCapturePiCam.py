# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:40:09 2017

@author: pi
"""
import sys
import os
import shutil
# Create Class for handling Pi Camera Frame Capture
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import time
import simpleMotionDetector

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

# cleanup motion capture dir
print("[INFO] cleaning up image folder")
shutil.rmtree('./motionCaptureImages', ignore_errors=True)
os.makedirs('./motionCaptureImages')

# create detector
print("[INFO] creating simple detector object")
detector = simpleMotionDetector.SimpleMotionDetector(debug=False, thresh_diff=10, avg_ratio=.5)

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream(resolution=(1920, 1080), framerate=30)
vs.start()
time.sleep(2.0)
frameCount = 0

# grab frames from threaded cam process
while 1 == 1:
    frameCount += 1

    # grab the frame from the threaded video stream and resize it
    frame = vs.read()
    frameSmall = cv2.resize(frame, None, fx=.3, fy=.3)

    # run motion detection
    (isMotion, procFrame) = detector.procFrame(frameSmall)

    # Create some text for the screen
    frameText = "Frame Count: %d" % frameCount
    cv2.putText(procFrame, frameText.format(frameText), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display to screen
    cv2.imshow("Frame", procFrame)
    if cv2.waitKey(1) == ord('q'):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

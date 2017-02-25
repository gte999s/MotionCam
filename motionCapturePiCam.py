# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:40:09 2017

@author: pi
"""
import sys
import os
# Import astral so we can get sunset/sunrise times
from astral import Astral
# Create Class for handling Pi Camera Frame Capture
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import multiprocessing
import time
import simpleMotionDetector
import GuasianMixtureModelMotionDetector
import imageWriter
import datetime

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

def imageGallaryTask():
    import time
    import subprocess
    
    while 1==1:
        time.sleep(60)
        subprocess.check_call(['sigal','build'])
    

def webserverTask():
    import SimpleHTTPServer
    import SocketServer
    import os
    
    PORT = 8000
    rootPath = "/home/pi/github/MotionCam/."
    
    os.chdir(rootPath)
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    
    print "serving folder: ", rootPath
    print "serving at port", PORT
    
    httpd.serve_forever()


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
        print "stopping frame capture process"

# Create sunrise/sunset dictionary for city
astral = Astral()
astral.solar_depression = 'civil'
city = astral['raleigh']

# create detector
print("[INFO] creating GMM detector object")
detector = GuasianMixtureModelMotionDetector.GMMMotionDetector(debug=True, history=1000, detectShadows=True)
# detector = simpleMotionDetector.SimpleMotionDetector(debug=False, thresh_diff=10, avg_ratio=.3, min_contour_size=500)

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream(resolution=(2592, 1944), framerate=15)
vs.start()
time.sleep(4.0)

# Start webserver
webThread = multiprocessing.Process(target=webserverTask, args=())
webThread.daemon = True
webThread.start()

# Start Gallery Updater
galleryThread = multiprocessing.Process(target=imageGallaryTask, args=())
galleryThread.daemon = True
galleryThread.start()

# Start Main Loop
saveThread = None
frameCount = 0
startTime = time.time()
captureFrameCount = 0
# grab frames from threaded cam process
while 1 == 1:
    frameCount += 1

    # get timestamp
    datestr = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    dateOnlyStr = datetime.datetime.now().strftime('%Y_%m_%d')

    # grab the frame from the threaded video stream and resize it
    frame = vs.read()
    frameSmall = cv2.resize(frame, None, fx=.22, fy=.22)
    frameSmall = frameSmall[100:,]


    # run motion detection
    (isMotion, procFrame) = detector.procFrame(frameSmall)

    # Create some text for the screen
    fps = frameCount / (time.time() - startTime)
    frameText = "Frame Count: % 6d FPS: %2.1f       %s" % (captureFrameCount , fps, datestr)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(procFrame, frameText, (10, 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    if saveThread is not None:
        if not saveThread.is_alive():
            saveThread = None
            print "Save Process Complete"
        else:
            print "Save Process running"

    if (isMotion or captureFrameCount <= 3) and saveThread is None:
        sun = city.sun(date=datetime.datetime.now(), local=True)
        tzinfo = sun['dusk'].tzinfo
        
        if sun['dawn'] < datetime.datetime.now(tzinfo) < sun['dusk']:        
        
            folderName = './images/' + dateOnlyStr + '/'
    
            # do folder maintenance
            if not os.path.isdir(folderName):
                # Reset Captured Frame Count each day
                captureFrameCount = 0
                # make folder for the current day
                os.makedirs(folderName)
    
            # Increment number of captured images for this day
            captureFrameCount += 1        
    
            # Finally make some JPEGs
            frameStr = folderName + 'I_%s_%d_LowRes.jpg' % (datestr, captureFrameCount)
            frameHighResStr = folderName + 'I_%s_%d_HighRes.jpg' % (datestr, captureFrameCount)

            saveThread = Thread(name="saveThread", target=imageWriter.writeNewImage, args=(100,
                                                                           procFrame,frameStr,
                                                                           frame,frameHighResStr))
            saveThread.daemon = True
            saveThread.start()
            print "Save Process started"


    # Display to screen
    cv2.imshow("Frame", procFrame)
    if cv2.waitKey(1) == ord('q'):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()




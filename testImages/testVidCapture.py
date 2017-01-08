from picamera import PiCamera
from picamera.array import PiRGBArray
import argparse
import warnings
import datetime

import json
import time

import argparse
import datetime

import time

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import imutils

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 2
camera.led = False
rawCapture = PiRGBArray(camera, size=(1920, 1088))
 
# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] warming up..."
time.sleep(2)
avg = None
lastUploaded = datetime.datetime.now()
count = 0	


# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
	frame = f.array
	timestamp = datetime.datetime.now()
	print timestamp
	

	
	if 1==1:
		# display the security feed
		#cv2.imshow("Security Feed", frame)
		key = cv2.waitKey(1) & 0xFF
 
		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
 

	cv2.imwrite("frame_" + str(count) + ".jpg", frame )
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	count=count+1
	
# cleanup the camera and close any open windows
camera.close()
cv2.destroyAllWindows()	
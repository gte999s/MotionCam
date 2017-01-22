import sys
from threading import Thread
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import time



class imageWriter:
    def __init__(self, quality=100):

        self.quality = quality
        self.frame = None
        self.frameStr = None
        self.frameHighRes = None
        self.frameHighResStr = None
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        # start the thread to poll for new images to write        
        self.thread.start()
        return self
        
    def isRunning(self):
        return self.thread.isAlive();

    def update(self):
        # Load images to SD Card
        cv2.imwrite(self.frameStr, self.frame,
                    [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        cv2.imwrite(self.frameHighResStr, self.frameHighRes,
                    [cv2.IMWRITE_JPEG_QUALITY, self.quality])


    def writeNewImage(self, frame = None, frameStr = None, frameHighRes = None, frameHighResStr = None):
        # Load new images to be written to SD CARD and toggle isRunning semaphore
        self.frame = frame
        self.frameStr = frameStr

        self.frameHighRes = frameHighRes
        self.frameHighResStr = frameHighResStr

        self.start()



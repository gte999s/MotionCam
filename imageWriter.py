import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy


class imageWriter:
    def __init__(self, quality=100):

        self.quality = quality
        self.frame = None
        self.frameStr = None
        self.frameHighRes = None
        self.frameHighResStr = None
        self.isRunning = False
        self.stopped = False

    def start(self):
        # start the thread to poll for new images to write
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Continuous loop checking for new files to be loaded to SD card
        while True:

            if self.isRunning:
                print "[INFO] writting new image to JPG %s", self.frameStr
                cv2.imwrite(self.frameStr, self.frame,
                            [cv2.IMWRITE_JPEG_QUALITY, self.quality])
                cv2.imwrite(self.frameHighResStr, self.frameHighRes,
                            [cv2.IMWRITE_JPEG_QUALITY, self.quality])
                self.frame = None
                self.frameHighRes = None
                self.isRunning = False

            if self.stopped:
                return

    def writeNewImage(self, frame = None, frameStr = None, frameHighRes = None, frameHighResStr = None):
        # Load new images to be written to SD CARD and toggle isRunning semaphore
        self.frame = frame
        self.frameStr = frameStr

        self.frameHighRes = frameHighRes
        self.frameHighResStr = frameHighResStr

        self.isRunning = True

    def stop(self):
        # set flag to kill update thread
        self.stopped = True

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

def writeNewImage(quality = 100, frame = None, frameStr = None, frameHighRes = None, frameHighResStr = None):
    # Load new images to be written to SD CARD
    cv2.imwrite(frameStr, frame,
               [cv2.IMWRITE_JPEG_QUALITY, quality])
    cv2.imwrite(frameHighResStr, frameHighRes,
               [cv2.IMWRITE_JPEG_QUALITY, quality])



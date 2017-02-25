import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy

class GMMMotionDetector:

    def __init__(self,thresh_diff=10, min_contour_size=1000, history=30, detectShadows= False, blur=(13, 13), debug=False):
        self.thresh_diff=thresh_diff
        self.min_contour_size=min_contour_size
        self.history = history
        self.blur = blur
        self.detectShadows = False
        self.gmmSubtractor = cv2.createBackgroundSubtractorMOG2(history=self.history, detectShadows= self.detectShadows)
        self.debug = debug

    def procFrame(self, frame):
        # Convert to Greyscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur a lot to get rid of noise
        # gray = cv2.GaussianBlur(gray, (13, 13), 0)

        # Run Gaussian Mixture Model Background Subtractor
        fg = self.gmmSubtractor.apply(frame)

        # find contours using the threshold image
        contours = cv2.findContours(fg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

        isMotion = False
        for c in contours:
            # ignore the contour if it's too small
            if cv2.contourArea(c) < self.min_contour_size:
                continue

            # If we are here, it means we've found a bit contour so there's motion
            isMotion = True

            # update image with contour if debug is on
            cv2.drawContours(frame, [c], 0, (255, 255, 255), 3)

        # show images if debug is on
        if self.debug:
            cv2.imshow("Frame", frame)
            cv2.imshow("FG", fg)

        return isMotion, frame

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

class simpleMotionDetector
    def __init__(self,thresh_diff=10,min_contour_size=1000,avg_ratio=0.7, blur=(13, 13), debug=False):
        self.thresh_diff=thresh_diff
        self.min_contour_size=min_contour_size
        self.avg_ratio=avg_ratio
        self.frame_avg=None
        self.blur = blur
        self.debug = debug

    def get_foreground(self, frame):
        # Convert to Greyscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur a lot to get rid of noise
        gray = cv2.GaussianBlur(gray, (13, 13), 0)

        # Init running average if not done already
        if self.frame_avg is None
            self.frame_avg = gray.copy().astype('float')

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, self.frame_avg, self.avg_ratio)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.frame_avg))

        # threshold the delta image
        # Erode the image to get rid of specs
        # dilate the thresholded image to fill in holes
        thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
        kernel = numpy.ones((5, 5), numpy.uint8)
        thresh = cv2.erode(thresh, kernel=kernel)
        thresh = cv2.dilate(thresh, None, iterations=10)

        # find contours using the threshold image
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

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
            cv2.imshow("Frame",frame)
            cv2.imshow("gray",gray)
            cv2.imshow("Frame Delta",frameDelta)
            cv2.imshow("Threshold",thresh)
            cv2.waitKey(1)



        return isMotion, frame
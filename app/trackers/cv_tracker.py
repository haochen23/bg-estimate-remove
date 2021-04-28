import cv2
import sys

sys.path.extend("../../")
from app.config import CV_TRACKER_TYPES as trackerTypes


def createTrackerByName(trackerType='KCF'):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.legacy.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.legacy.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.legacy.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.legacy.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.legacy.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.legacy.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.legacy.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker


class CVTracker:
    def __init__(self):

        self.n_objects = None

    def initialize_trackers(self, frame, rects, tracker='KCF'):
        self.multi_tracker = cv2.legacy.MultiTracker_create()
        for rect in rects:
            self.multi_tracker.add(createTrackerByName(tracker), frame, tuple(rect))
        self.n_objects = len(rects)

    def update(self, frame, rects):
        if len(rects) == self.n_objects:
            success, boxes = self.multi_tracker.update(frame)
            return success, boxes
        else:
            self.initialize_trackers(frame, rects, tracker='KCF')
            return self.update(frame, rects)

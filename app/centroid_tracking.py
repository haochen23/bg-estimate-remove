import sys

sys.path.extend("../")

from app.utils.foreground import get_fg_mask
from app.utils.background import calculate_background

from app.trackers.centroid_tracker import CentroidTracker
from app.config import MAX_DISAPPEAR_FRAME_COUNTS, MAX_OBJECT_DIST, START_X, START_Y, END_X, END_Y

import cv2

if __name__ == '__main__':
    video = 'video.mp4'
    bg = calculate_background(video)
    ret = True
    cap = cv2.VideoCapture(video)
    ct = CentroidTracker(max_disappearance=MAX_DISAPPEAR_FRAME_COUNTS)
    while ret:
        ret, frame = cap.read()
        if not ret:
            break
        height, width = frame.shape[:2]
        rects, fg_mask = get_fg_mask(frame, bg)
        cv2.rectangle(frame, (int(START_X * width), int(START_Y * height)), (int(END_X * width), int(END_Y * height)),
                      (0, 0, 255), 2)
        for (start_x, start_y, end_x, end_y) in rects:
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        objects = ct.update(rects)

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # cv2.imshow("Frame", frame)
        # cv2.imshow('fg_mask', fg_mask)
        # cv2.waitKey(0)

    cv2.destroyAllWindows()
    # cap.release()

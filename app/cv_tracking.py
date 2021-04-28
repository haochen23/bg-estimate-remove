import cv2
import sys

sys.path.extend("../")
from app.config import CV_TRACKER_TYPES as trackerTypes
from app.utils.background import calculate_background
from app.utils.foreground import get_fg_mask
from app.trackers.cv_tracker import createTrackerByName, CVTracker

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Path to a video file, or camera index.")
    parser.add_argument("--n_frames", type=int, default=25, help="Number of frames used to calculate background")
    parser.add_argument("--tracker", type=str, default="KCF",
                        help="Which type of tracker to use, available types are listed in config.")
    args = parser.parse_args()

    video = args.video
    bg = calculate_background(video, n_frames=args.n_frames)
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    assert ret, "Camera or video feed read failed."
    rects, fg_mask = get_fg_mask(frame, bg)
    for i in range(len(rects)):
        rects[i][2] -= rects[i][0]
        rects[i][3] -= rects[i][1]
    tracker = CVTracker()
    tracker.initialize_trackers(frame, rects, tracker='KCF')
    tracker.update(frame, rects)

    while ret:
        ret, frame = cap.read()
        if not ret:
            break
        rects, fg_mask = get_fg_mask(frame, bg)
        for i in range(len(rects)):
            rects[i][2] -= rects[i][0]
            rects[i][3] -= rects[i][1]
        success, boxes = tracker.update(frame, rects)
        # print(success)
        if len(boxes) > 0:
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)

        # cv2.imshow('MultiTracker', frame)

        # quit on ESC button
        # if cv2.waitKey(0) & 0xFF == 27:  # Esc pressed
        #     break

    cv2.destroyAllWindows()
    cap.release()

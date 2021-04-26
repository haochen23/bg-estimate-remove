"""Calibrate background from camera stream or a background video file."""

import numpy as np
import cv2
import sys
sys.path.append("../")

def calculate_background(video="background.mp4", n_frames=25):
    """
    Estimate background from
    :param video: int or str, if int - camera index, if str, path to a video file
    :param n_frames: number of frame used for background estimation
    :return:
        bg: estimated background, grayscale
    """

    cap = cv2.VideoCapture(video)
    frames = []
    if isinstance(video, int):
        # read the first n_frames
        count = 0
        while count < n_frames:
            ret, frame = cap.read()
            frames.append(frame)
            count += 1
    elif isinstance(video, str):
        # randomly read n_frames
        frame_ids = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=n_frames)
        for fid in frame_ids:
            cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
            ret, frame = cap.read()
            frames.append(frame)
    else:
        raise TypeError(f'Wrong type {video}, must be either int or str.')

    # Calculate the median along the time axis
    median_bg = np.median(frames, axis=0).astype(dtype=np.uint8)
    bg = cv2.cvtColor(median_bg, cv2.COLOR_BGR2GRAY)

    return bg


if __name__ == '__main__':
    import argparse
    from PIL import Image
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Path to a video file, or camera index.")
    parser.add_argument("--n_frames", type=int, default=25, help="Number of frames used to calculate background")

    args = parser.parse_args()
    try:
        args.video = int(args.video)
    except Exception:
        pass

    bg = calculate_background(video=args.video, n_frames=args.n_frames)
    bg = Image.fromarray(bg, mode='L')
    bg.show()

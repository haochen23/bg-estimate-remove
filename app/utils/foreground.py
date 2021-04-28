import numpy as np
import cv2
import sys

sys.path.extend("../../")
from app.config import MIN_CONTOUR_AREA
from app.config import START_X, START_Y, END_X, END_Y

SQUARE_KERNEL_SMALL = np.ones([3, 3], dtype=np.uint8)
SQUARE_KERNEL_LARGE = np.ones([7, 7], dtype=np.uint8)


def get_fg_mask(img, bg_img):
    """
    Calculate foreground mask
    :param img: cv2 bgr image contain foreground and background
    :param bg_img: background image grayscale, numpy array
    :return:
        fg_mask: binary foreground mask
    """
    assert img.shape[:2] == bg_img.shape[:2]
    height, width = img.shape[:2]

    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    assert len(img.shape) == 2 and len(bg_img.shape) == 2
    diff = cv2.absdiff(img, bg_img)

    _, fg_mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel=SQUARE_KERNEL_SMALL, iterations=1)
    # fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_ERODE, kernel=SQUARE_KERNEL_SMALL, iterations=1)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel=SQUARE_KERNEL_LARGE, iterations=3)

    contours, _ = cv2.findContours(fg_mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    if len(contours) > 0:

        for contour in contours:
            if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                cX = int((x + x + w) / 2.0)
                cY = int((y + y + h) / 2.0)

                if height * START_Y < cY <= height * END_Y and width * START_X < cX <= width * END_X:
                    rects.append([x, y, x + w, y + h])
    return rects, fg_mask


def remove_background(img, fg_mask):
    return cv2.bitwise_and(img, img, mask=fg_mask)


if __name__ == '__main__':
    from app.utils.background import calculate_background

    video = 'video.mp4'
    bg = calculate_background(video)
    ret = True
    cap = cv2.VideoCapture(video)
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

        # cv2.imshow("Frame", frame)
        # cv2.imshow('fg_mask', fg_mask)
        # cv2.waitKey(0)

        # fg = remove_background(frame, fg_mask)
        #
        # cv2.imshow('fg', fg)
        # cv2.waitKey(50)

    cap.release()
    cv2.destroyAllWindows()

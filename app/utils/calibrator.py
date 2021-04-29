"""Recalculate background images for camera feed when there is a number of frames has very little difference
than the previious background image.

It uses the new frames to recalculate a new grayscale background image"""


import cv2
import numpy as np
import sys

sys.path.extend("../../")

from app.config import MAX_CONSECUTIVE_BG, THRESH_PIXEL_CHANGE


class Calibrator:
    def __init__(self, bg_img, max_consecutive_bg=MAX_CONSECUTIVE_BG):
        """

        :param bg_img: initial background image, grayscale
        :param max_consecutive_bg: consecutive number of background-like frames
        """
        self.frames = [None] * max_consecutive_bg
        self.bg_img = bg_img
        self.max_consecutive_bg = max_consecutive_bg
        self.counter = 0

    def run(self, img):
        """

        :param img: a regular bgr frame
        :return:
        """
        assert img.shape[:2] == self.bg_img.shape[:2]
        # height, width = img.shape[:2]

        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(img.copy(), self.bg_img)
        _, fg_mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        if np.sum(fg_mask / 255) <= THRESH_PIXEL_CHANGE:
            self.frames[self.counter] = img
            self.counter += 1
        else:
            for i in range(self.counter):
                self.frames[i] = None
            self.counter = 0

        if self.counter >= self.max_consecutive_bg:
            # recalculate background image
            self.bg_img = np.median(self.frames, axis=0).astype(dtype=np.uint8)
            for i in range(self.max_consecutive_bg):
                self.frames = None

            self.counter = 0
            return self.bg_img

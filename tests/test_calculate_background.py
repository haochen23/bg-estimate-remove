from app.utils.background import calculate_background
import numpy as np


def test_calculate_background():
    video = "video.mp4"
    bg = calculate_background(video=video, n_frames=25)
    assert type(bg) == np.ndarray
    assert len(bg.shape) == 2

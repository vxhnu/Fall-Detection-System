# camera.py
import cv2

def get_video_capture(path):
    """
    Returns a cv2.VideoCapture object for the given file path.
    """
    return cv2.VideoCapture(path)

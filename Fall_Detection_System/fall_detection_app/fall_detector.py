# fall_detector.py
import math
from config import ANGLE_THRESHOLD, DROP_THRESHOLD

def compute_torso_angle(mid_sh, mid_hip):
    """
    Computes the angle of the torso (shoulder-to-hip line) relative to vertical.
    Returns angle in degrees.
    """
    dx = mid_sh[0] - mid_hip[0]
    dy = mid_sh[1] - mid_hip[1]
    # Angle relative to vertical: use arctan2(dx, dy)
    angle = abs(math.degrees(math.atan2(dx, dy)))
    return angle

def compute_hip_drop(mid_sh, mid_hip, frame_height):
    """
    Computes normalized hip drop as (hip_y - shoulder_y) / frame_height.
    """
    drop = (mid_hip[1] - mid_sh[1]) / frame_height
    return drop

def is_fall(mid_sh, mid_hip, frame_height):
    """
    Returns True if the torso angle and hip drop exceed thresholds.
    """
    angle = compute_torso_angle(mid_sh, mid_hip)
    drop = compute_hip_drop(mid_sh, mid_hip, frame_height)
    # A fall is flagged if both conditions are met
    return angle > ANGLE_THRESHOLD and drop > DROP_THRESHOLD

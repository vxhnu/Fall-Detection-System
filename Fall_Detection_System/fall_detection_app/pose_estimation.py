# pose_estimation.py
import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)  # Use default settings

def get_pose_landmarks(frame):
    """
    Runs MediaPipe Pose on the frame and returns shoulder and hip midpoints.
    Returns ((mid_sh_x, mid_sh_y), (mid_hip_x, mid_hip_y))
    or None if no person is detected.
    """
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)  # Perform pose detection:contentReference[oaicite:6]{index=6}

    if results.pose_landmarks:
        h, w, _ = frame.shape
        lm = results.pose_landmarks.landmark
        # Landmark indices for shoulders and hips in MediaPipe:
        # Left shoulder=11, Right shoulder=12, Left hip=23, Right hip=24
        left_sh = lm[11]; right_sh = lm[12]
        left_hip = lm[23]; right_hip = lm[24]
        # Convert normalized coordinates to pixel values
        ls_x, ls_y = int(left_sh.x * w), int(left_sh.y * h)
        rs_x, rs_y = int(right_sh.x * w), int(right_sh.y * h)
        lh_x, lh_y = int(left_hip.x * w), int(left_hip.y * h)
        rh_x, rh_y = int(right_hip.x * w), int(right_hip.y * h)
        # Compute midpoints of shoulders and hips
        mid_sh_x = (ls_x + rs_x) // 2
        mid_sh_y = (ls_y + rs_y) // 2
        mid_hip_x = (lh_x + rh_x) // 2
        mid_hip_y = (lh_y + rh_y) // 2
        return (mid_sh_x, mid_sh_y), (mid_hip_x, mid_hip_y)
    else:
        return None

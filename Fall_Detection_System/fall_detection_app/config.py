# config.py

# --- Email Settings (set your Gmail credentials) ---
EMAIL_ADDRESS = "timepasskeliye036@gmail.com"      # Your Gmail address
EMAIL_PASSWORD = "dtun hepf jtif iiry"        # Your Gmail app password (not regular password)
RECEIVER_EMAIL = "vishnu.rameshan03@gmail.com"  # Where alert emails will be sent
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- File Upload Settings ---
UPLOAD_FOLDER = "uploads"     # Folder to store uploaded videos
OUTPUT_FOLDER = "static/videos"  # Folder to save annotated videos
ALLOWED_EXTENSIONS = {"mp4", "avi"}  # Permitted file extensions

# --- Fall Detection Thresholds ---
ANGLE_THRESHOLD = 45       # Torso angle threshold in degrees
DROP_THRESHOLD = 0.20      # Hip drop threshold (20% of frame height)
FALL_FRAME_COUNT = 5       # Minimum consecutive frames to confirm a fall

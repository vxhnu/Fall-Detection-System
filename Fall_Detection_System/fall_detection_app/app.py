# app.py
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from camera import get_video_capture
from detection import detect_people
from pose_estimation import get_pose_landmarks
from fall_detector import is_fall
from logger import log_event, get_events
from alert import send_email_alert
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS, FALL_FRAME_COUNT

import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Handles the upload form and video processing.
    """
    if request.method == 'POST':
        # Check if a file part is present
        if 'video' not in request.files:
            return redirect(request.url)
        file = request.files['video']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Secure the filename and save to uploads/
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)  # Save the uploaded video:contentReference[oaicite:8]{index=8}

            # Prepare to process video
            cap = get_video_capture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_size = (width, height)

            # Set up output video writer (XVID codec for AVI)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_filename = f"output_{filename.rsplit('.',1)[0]}.avi"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

            fall_counter = 0
            fall_detected = False

            # Process each frame
            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # End of video

                # 1. Detect people in the frame
                persons = detect_people(frame)

                # 2. For simplicity, check each detected person
                for (x1, y1, x2, y2) in persons:
                    # Crop to the person's region (optional; here we use full frame for pose)
                    # 3. Estimate pose for the frame/person
                    pose_data = get_pose_landmarks(frame)
                    if pose_data:
                        (mid_sh_x, mid_sh_y), (mid_hip_x, mid_hip_y) = pose_data
                        # 4. Apply fall detection logic
                        if is_fall((mid_sh_x, mid_sh_y), (mid_hip_x, mid_hip_y), height):
                            fall_counter += 1
                        else:
                            fall_counter = 0

                        # If condition holds for enough frames, register a fall
                        if fall_counter >= FALL_FRAME_COUNT and not fall_detected:
                            fall_detected = True
                            # Overlay text on the frame
                            cv2.putText(frame, "FALL DETECTED", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                            # Log to database and send alert
                            log_event(filename, "Offline")
                            send_email_alert(filename)
                        elif fall_detected:
                            # If already detected, keep overlay
                            cv2.putText(frame, "FALL DETECTED", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    break  # Process only the first person for simplicity

                # Write the (possibly annotated) frame to output video
                out.write(frame)

            # Release resources
            cap.release()
            out.release()

            # Render output page with link to annotated video
            return render_template('output.html', filename=output_filename)

    # GET request: show upload form
    return render_template('upload.html')

@app.route('/videos/<path:filename>')
def download_file(filename):
    """
    Serves the output video files from the static/videos folder.
    """
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/logs')
def show_logs():
    """
    Displays a table of all fall events from the database.
    """
    events = get_events()
    return render_template('logs.html', events=events)

@app.route('/')
def index():
    """
    Redirect root to upload page.
    """
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)

# detection.py
from ultralytics import YOLO

# Load the YOLOv8n model (pre-trained on COCO dataset)
model = YOLO("yolov8n.pt")  # You can use other weights if available

def detect_people(frame):
    """
    Detects people in the frame using YOLOv8.
    Returns a list of bounding boxes [x1, y1, x2, y2] for each detected person.
    """
    results = model(frame)  # Run detection on the frame:contentReference[oaicite:4]{index=4}
    boxes = []
    for result in results:
        # result.boxes contains all detected objects in this frame
        for box in result.boxes:
            cls = int(box.cls[0]) if box.cls.ndim else int(box.cls)
            name = result.names[cls]  # Get class name (e.g. 'person')
            if name == "person":
                x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coords
                # Convert to integers for drawing
                boxes.append((int(x1), int(y1), int(x2), int(y2)))
    return boxes

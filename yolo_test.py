import os
from ultralytics import YOLO
import cv2

# Define directories and file paths
VIDEOS_DIR = os.path.join('.', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'testvideo.mp4')
video_path_out = os.path.join(VIDEOS_DIR, 'testvideo_out.mp4')

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read the first frame to get frame dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Could not read the first frame of the video.")
    exit()
H, W, _ = frame.shape

# Create a VideoWriter object to save the annotated video
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

# Load the trained model
model = YOLO('yolomodels/animals-4/detect/train/weights/best.pt')

# Define detection threshold
threshold = 0.5

# Process each frame of the video
while ret:
    # Perform object detection on the frame
    results = model(frame)[0]

    # Draw bounding boxes on the frame
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Write the annotated frame to the output video
    out.write(frame)

    # Read the next frame
    ret, frame = cap.read()

# Release the video capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()

print('Video test completed successfully!')

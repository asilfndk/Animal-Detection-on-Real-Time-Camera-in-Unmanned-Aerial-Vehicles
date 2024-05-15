import cv2
from ultralytics import YOLO

def detect_objects_in_video(video_path, output_path, model_path):
    # Load the YOLOv8 model
    model = YOLO(model_path)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        # Render the results on the frame
        annotated_frame = results[0].plot()

        # Write the frame to the output video file
        out.write(annotated_frame)

        # Display the frame with detection (optional)
        cv2.imshow('Object Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Define input and output video paths and model path
    input_video_path = 'videos/testvideo.mp4'
    output_video_path = 'videos/output_video.mp4'
    model_path = 'yolomodels/cattle/detect/train/weights/best.pt'

    # Run the object detection on the video
    detect_objects_in_video(input_video_path, output_video_path, model_path)

#!/usr/bin/python3

import os
import cv2
from ultralytics import YOLO

def process_video(input_path, output_path, model_path="best.pt"):
    """
    Processes a video with YOLO object detection and saves the annotated video.
    """
    # Load the YOLO model
    model = YOLO(model_path)

    # Open the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video file: {input_path}")

    # Prepare the output video writer
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    print(f"Processing video: {input_path}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference on the frame
        results = model(frame)

        # Annotate the frame with detection results
        annotated_frame = results[0].plot()

        # Write the annotated frame to the output video
        out.write(annotated_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Video processing completed. Annotated video saved to {output_path}")

# Define paths
video_path = "termica.MP4"
output_path = "annotated_video.mp4"
model_path = "best.pt"

# Process the video
process_video(video_path, output_path, model_path)

#!/usr/bin/python3

import os
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("best.pt")

# Path to the folder containing test images
test_folder = "data/val/images"

# Get a list of all image files in the test folder
# Supports common image formats like .jpg, .png, .jpeg
image_files = [
    os.path.join(test_folder, file)
    for file in os.listdir(test_folder)
    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))
]

# Run batched inference on the list of images
results = model("termica.MP4")  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Bounding box outputs
    masks = result.masks  # Segmentation mask outputs
    keypoints = result.keypoints  # Pose outputs
    probs = result.probs  # Classification probabilities
    obb = result.obb  # Oriented bounding boxes

    result.show()  # Display to screen
    input()
    
    
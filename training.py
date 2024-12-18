from ultralytics import YOLO

# Load a model

model = YOLO("yolov8s.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="/home/santi/detector_base/yolov8_full_model/data.yaml", epochs=100, imgsz=640, augment=True)
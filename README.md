# **Bolt Joint Detection**

This reposity it's created as deliberable for the project started along Cobra for detecting failures on thermosolar panels.

---

## **Repository Contents**

1. **YOLO Module**
   - Description of the trained YOLO module and its functionality.
   - Instructions on how to use it for video processing.

2. **Dataset**
   - Details of the dataset used to train YOLO.
   - Dataset source (if applicable).
   - Guide on adding or modifying data for re-training the model.

3. **Video Processing**
   - Description of the script for video processing.
   - Expected input format (e.g., video files).
   - Generated output (e.g., processed images or data).

4. **Map Generation**
   - Description of the script for generating pre-processing maps.
   - Input and output formats.
   - Its relation to the YOLO module.

---

## **Prerequisites**

List of tools, libraries, and frameworks needed to run the project:

- Python (recommended version).
- TensorFlow/PyTorch (depending on YOLO backend).
- OpenCV, NumPy, Matplotlib, etc.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the YOLO model weights:
   - Link or steps to download the trained model weights.

---

## **Usage**

### **1. Generate Pre-Processing Maps**
Run the map generation script:
```bash
python generate_maps.py --input input_folder --output output_folder
```

### **2. Process Videos with YOLO**
Run the video processing script:
```bash
python process_videos.py --video video.mp4 --output results/
```

### **3. Train YOLO (Optional)**
If you want to re-train the model, follow these steps:
```bash
python train_yolo.py --dataset path_to_dataset --epochs 50
```

---


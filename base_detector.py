import csv
import cv2
import os
from ultralytics import YOLO

def process_crops_with_yolo_and_store_percentage(csv_path, model_path):
    """
    Processes each crop listed in the CSV using a YOLO model, calculates the relative percentage of the
    CSV's center X coordinate with respect to the X1-X2 range of each detection, annotates the results on the image,
    and saves an additional CSV for tracking purposes.
    """
    try:
        # Load YOLO model
        model = YOLO(model_path)
        print(f"Loaded YOLO model from: {model_path}")

        # Open the CSV file
        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Ensure `procesados` folder exists
            crops_base_path = os.path.dirname(csv_path)
            procesados_path = os.path.join(crops_base_path, 'procesados')
            os.makedirs(procesados_path, exist_ok=True)

            # Create the output tracking CSV
            tracking_csv_path = os.path.join(procesados_path, 'tracking_results.csv')
            with open(tracking_csv_path, mode='w', newline='') as tracking_csv_file:
                tracking_writer = csv.writer(tracking_csv_file)
                tracking_writer.writerow(["colector", "percentage", "processed_image"])  # Header row

                # Process each row in the input CSV
                for row in csv_reader:
                    if len(row) != 5:
                        print(f"Skipping invalid row: {row}")
                        continue

                    colector, frame_number, relative_center_x, relative_center_y, image_path = row

                    # Convert coordinates to integers
                    relative_center_x = int(relative_center_x)

                    # Check if the image exists
                    if not os.path.exists(image_path):
                        print(f"Image not found: {image_path}")
                        continue

                    # Load the crop image
                    image = cv2.imread(image_path)

                    # Draw the circle at the center from the CSV
                    cv2.circle(image, (relative_center_x, int(relative_center_y)), radius=10, color=(0, 0, 255), thickness=-1)

                    # Annotate the colector name
                    cv2.putText(image, f"Colector: {colector}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # Process the image with YOLO
                    results = model(image)
                    detections = results[0].boxes.xyxy.cpu().numpy()  # Get all detections (X1, Y1, X2, Y2)

                    # Compare the X from the CSV to the range of X1-X2 for each detection
                    for detection in detections:
                        x1, y1, x2, y2 = map(int, detection[:4])  # Extract bounding box coordinates

                        # Calculate the relative percentage along the X-axis
                        if x1 < x2:  # Ensure X1 is less than X2
                            percentage_x = ((relative_center_x - x1) / (x2 - x1)) * 100

                            # Annotate the percentage on the image
                            label = f"{percentage_x:.2f}% from left"
                            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            # Write the tracking data to the CSV
                            output_filename = f"processed_{os.path.basename(image_path)}"
                            output_path = os.path.join(procesados_path, output_filename)
                            tracking_writer.writerow([colector, f"{percentage_x:.2f}", output_path])

                        # Draw the bounding box for visualization
                        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    # Save the processed image in the `procesados` folder
                    output_filename = f"processed_{os.path.basename(image_path)}"
                    output_path = os.path.join(procesados_path, output_filename)
                    cv2.imwrite(output_path, image)
                    print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_all_folders_in_salida_with_yolo(base_path='./salida', model_path='best.pt'):
    """
    Iterates through all folders in the base `salida` directory to find and process `bbox_centers.csv` files
    using a YOLO model.
    """
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.isdir(folder_path):
            continue  # Skip files, only process directories

        csv_path = os.path.join(folder_path, 'crops_base', 'bbox_centers.csv')
        if os.path.exists(csv_path):
            print(f"Processing CSV: {csv_path}")
            process_crops_with_yolo_and_store_percentage(csv_path, model_path)
        else:
            print(f"No CSV found in: {folder_path}")

# Example usage
if __name__ == "__main__":
    # Base path to the `salida` folder and the YOLO model path
    salida_path = './salida'
    yolo_model_path = 'DetectorBases.pt'
    process_all_folders_in_salida_with_yolo(salida_path, yolo_model_path)

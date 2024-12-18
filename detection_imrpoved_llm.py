import cv2
import os
import math
from ultralytics import YOLO

# from MODULOS.Identificar_Colector import identificar_colector, obtener_coordenadas
from MODULOS.Utilidades import hconcat_resize, buscar_videos_figuras


def zoom_frame(frame, zoom_factor=1):
    """Apply a zoom effect by cropping the center and resizing."""
    height, width = frame.shape[:2]
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    x1 = (width - new_width) // 2
    y1 = (height - new_height) // 2
    x2 = x1 + new_width
    y2 = y1 + new_height
    cropped_frame = frame[y1:y2, x1:x2]
    return cv2.resize(cropped_frame, (width, height), interpolation=cv2.INTER_LINEAR)


def calculate_angle(a, b, c):
    """Calculate the angle (in degrees) at vertex 'a' in the triangle formed by points a, b, c."""
    ab = math.dist(a, b)
    ac = math.dist(a, c)
    bc = math.dist(b, c)
    return math.degrees(math.acos((ab**2 + ac**2 - bc**2) / (2 * ab * ac)))


def get_color_based_on_angle(angle):
    """Return the color based on the angle value."""
    if angle > 130:
        return (0, 0, 255)  # Red
    elif 125 <= angle <= 130:
        return (0, 165, 255)  # Orange
    else:
        return (0, 255, 0)  # Green


def draw_largest_angle_and_color(frame, points, output_file):
    """Draw the triangle with colored lines and circles based on the largest angle."""
    angle_0 = calculate_angle(points[0], points[1], points[2])
    angle_1 = calculate_angle(points[1], points[0], points[2])
    angle_2 = calculate_angle(points[2], points[0], points[1])
    largest_angle = max((angle_0, 0), (angle_1, 1), (angle_2, 2))
    angle_value, vertex_index = largest_angle

    with open(output_file, "a") as f:
        f.write(f"Largest Angle: {int(angle_value)} deg\n")

    color = get_color_based_on_angle(angle_value)
    cv2.line(frame, points[0], points[1], color=color, thickness=2)
    cv2.line(frame, points[1], points[2], color=color, thickness=2)
    cv2.line(frame, points[2], points[0], color=color, thickness=2)
    for point in points:
        cv2.circle(frame, point, radius=10, color=color, thickness=2)

    vertex = points[vertex_index]
    cv2.putText(frame, f'{int(angle_value)} deg', vertex, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return frame


def parse_detections(detections, class_names):
    """Parse YOLO detections into a list of (label, confidence, bbox) tuples."""
    parsed_detections = []
    for i in range(len(detections.cls)):
        cls_id = int(detections.cls[i].item())
        confidence = float(detections.conf[i].item())
        bbox = detections.xyxy[i].tolist()
        label = class_names[cls_id] if cls_id < len(class_names) else "Unknown"
        parsed_detections.append((label, confidence, bbox))
    return parsed_detections


def draw_detections_and_triangle(frame, detections, output_file):
    """Process detections to calculate angles if four different classes are detected."""
    points = {}
    for label, confidence, bbox in detections:
        if label not in points:
            x1, y1, x2, y2 = map(int, bbox)
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            points[label] = center
        if len(points) == 4:  # Ensure we only process when 4 distinct classes are detected
            break

    if len(points) == 4:
        frame = draw_largest_angle_and_color(frame, list(points.values()), output_file)

    return frame


def main():
    try:
        videos_para_analizar = buscar_videos_figuras("./VIDEOS")
        if not videos_para_analizar:
            print('No hay videos para analizar')
            return
        
        zoom_factor = 1
        model_path = 'best.pt'
        model = YOLO(model_path)
        class_names = model.names  # List of class names from YOLO
        
        for video_para_analizar in videos_para_analizar:
            try:
                frame_actual = 0
                print(f"Processing video: {video_para_analizar}")
                path_video_completo = video_para_analizar
                carpeta_salida = './salida/' + os.path.basename(video_para_analizar).split('.')[0]

                if not os.path.exists(carpeta_salida):
                    os.makedirs(carpeta_salida)

                output_file = os.path.join(carpeta_salida, 'angles_output.txt')
                cap = cv2.VideoCapture(path_video_completo)
                if not cap.isOpened():
                    print(f"Error opening video file: {path_video_completo}")
                    continue

                while cap.isOpened():
                    ret_prev = None
                    ret_post = None
                    ret, frame = cap.read()
                    if not ret:
                        break

                    results = model(frame)
                    detections = results[0].boxes
                    parsed_detections = parse_detections(detections, class_names)
                    # Initialize a set to track unique classes
                    unique_classes = set()

                    # Iterate through parsed detections and add class names to the set
                    for detection in parsed_detections:
                        class_name = detection[0]  # The class is the first element in each tuple
                        unique_classes.add(class_name)

                    # Check if there are exactly 4 unique classes
                    if len(unique_classes) == 4:
                        detected_frame = draw_detections_and_triangle(frame, parsed_detections, output_file)

                        # Retrieve previous and post frames
                        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_actual - 15))
                        ret_prev, frame_prev = cap.read()
                        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_actual + 15)
                        ret_post, frame_post = cap.read()

                        if ret_prev and ret_post:
                            combined_frames = hconcat_resize([frame_prev, detected_frame, frame_post])
                            output_image_path = f'{carpeta_salida}/frame_{frame_actual}_combined.jpg'
                            cv2.imwrite(output_image_path, combined_frames)
                            print(f"Saved combined frame at: {output_image_path}")
                        
                        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_actual)

                    frame_actual += 1

                cap.release()

            except Exception as e:
                print(f"Error processing video {video_para_analizar}: {e}")

    except Exception as e:
        print(f"Error in main function: {e}")


if __name__ == "__main__":
    main()

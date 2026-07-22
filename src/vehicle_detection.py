import cv2
import pandas as pd
from ultralytics import YOLO
import src.config as config

def run_detection(video_path):
    print(f"Loading YOLO model for {video_path.name}...")
    model = YOLO(config.YOLO_MODEL)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {video_path}")
        
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    annotated_video_path = config.OUTPUTS_DIR / f"annotated_{video_path.name}"
    out = cv2.VideoWriter(str(annotated_video_path), fourcc, fps, (width, height))
    
    detections = []
    frame_count = 0
    
    print("Starting vehicle detection and tracking...")
    target_classes = [2, 3, 5, 7]
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        timestamp = frame_count / fps

        results = model.track(frame, persist=True, tracker=config.TRACKER, classes=target_classes, conf=config.CONFIDENCE_THRESHOLD, verbose=False)
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            clss = results[0].boxes.cls.cpu().numpy().astype(int)
            confs = results[0].boxes.conf.cpu().numpy()
            
            for box, track_id, cls, conf in zip(boxes, ids, clss, confs):
                vehicle_type = model.names[cls]
                detections.append({
                    "timestamp": round(timestamp, 2),
                    "vehicle_id": track_id,
                    "vehicle_type": vehicle_type,
                    "confidence": round(float(conf), 2)
                })

        annotated_frame = results[0].plot()
        out.write(annotated_frame)
        
        if frame_count % 100 == 0:
            print(f"Processed {frame_count} frames...")
            
    cap.release()
    out.release()
    
    print(f"Saving detections to {config.DETECTIONS_CSV_PATH}")
    df = pd.DataFrame(detections)
    if not df.empty:
        df.to_csv(config.DETECTIONS_CSV_PATH, index=False)
    else:
        print("Warning: No vehicles detected.")
        df = pd.DataFrame(columns=["timestamp", "vehicle_id", "vehicle_type", "confidence"])
        df.to_csv(config.DETECTIONS_CSV_PATH, index=False)
        
if __name__ == "__main__":
    run_detection()

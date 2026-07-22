import pandas as pd
import random
import src.config as config

def generate_mock_detections():
    print("Generating mock vehicle detections due to YOLO/Torch error...")

    detections = []
    vehicle_id_counter = 1
    
    vehicle_types = ['car', 'car', 'car', 'motorcycle', 'motorcycle', 'truck', 'bus']
    
    for _ in range(100):
        start_time = random.uniform(0, 300)
        v_type = random.choice(vehicle_types)
        v_id = vehicle_id_counter
        vehicle_id_counter += 1
        
        duration = random.uniform(2, 10)
        end_time = start_time + duration
        
        current_time = start_time
        while current_time <= end_time:
            detections.append({
                "timestamp": round(current_time, 2),
                "vehicle_id": v_id,
                "vehicle_type": v_type,
                "confidence": round(random.uniform(0.7, 0.99), 2)
            })
            current_time += 1/30.0 
            
    df = pd.DataFrame(detections)
    df = df.sort_values(by="timestamp")
    df.to_csv(config.DETECTIONS_CSV_PATH, index=False)
    print(f"Mock detections saved to {config.DETECTIONS_CSV_PATH}")

if __name__ == "__main__":
    generate_mock_detections()

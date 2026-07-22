import pandas as pd
import datetime
import src.config as config

def run_etl(video_path):
    print(f"Extracting data from {config.DETECTIONS_CSV_PATH}")
    
    try:
        df = pd.read_csv(config.DETECTIONS_CSV_PATH)
    except FileNotFoundError:
        print("Error: detections file not found. Run vehicle_detection first.")
        return
        
    if df.empty:
        print("Empty detections file.")
        pd.DataFrame(columns=['minute', 'vehicle_type', 'vehicle_count']).to_csv(config.TRAFFIC_PER_MINUTE_CSV_PATH, index=False)
        pd.DataFrame(columns=['datetime', 'date', 'hour', 'weekday', 'minute_offset', 'vehicle_type', 'vehicle_count', 'camera', 'road', 'city']).to_csv(config.PROCESSED_DATA_DIR / "enriched_traffic.csv", index=False)
        return
        
    unique_vehicles = df.groupby('vehicle_id').agg({
        'timestamp': 'min',
        'vehicle_type': 'first'
    }).reset_index()
    
    unique_vehicles['minute'] = (unique_vehicles['timestamp'] // 60).astype(int)
    
    traffic_per_minute = unique_vehicles.groupby(['minute', 'vehicle_type']).size().reset_index(name='vehicle_count')
    
    print(f"Saving aggregated traffic to {config.TRAFFIC_PER_MINUTE_CSV_PATH}")
    traffic_per_minute.to_csv(config.TRAFFIC_PER_MINUTE_CSV_PATH, index=False)
    
    print("Transforming data for Warehouse...")
    
    camera_folder = video_path.parent.name
    if camera_folder in config.CAMERAS:
        cam_meta = config.CAMERAS[camera_folder]
        camera_name = cam_meta['camera_name']
        road_name = cam_meta['road']
        city_name = cam_meta['city']
    else:
        camera_name = "Unknown Camera"
        road_name = "Unknown Road"
        city_name = "Unknown City"
        
    base_time = datetime.datetime.now()
    
    enriched_data = []
    
    for _, row in traffic_per_minute.iterrows():
        record_time = base_time + datetime.timedelta(minutes=int(row['minute']))
        
        enriched_data.append({
            'datetime': record_time.strftime('%Y-%m-%d %H:%M:%S'),
            'date': record_time.strftime('%Y-%m-%d'),
            'hour': record_time.hour,
            'weekday': record_time.strftime('%A'),
            'minute_offset': row['minute'],
            'vehicle_type': row['vehicle_type'],
            'vehicle_count': row['vehicle_count'],
            'camera': camera_name,
            'road': road_name,
            'city': city_name
        })
        
    enriched_df = pd.DataFrame(enriched_data)
    
    enriched_csv_path = config.PROCESSED_DATA_DIR / "enriched_traffic.csv"
    enriched_df.to_csv(enriched_csv_path, index=False)
    print(f"Enriched data saved to {enriched_csv_path}")

if __name__ == "__main__":
    run_etl()

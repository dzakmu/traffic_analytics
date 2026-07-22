import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.vehicle_detection import run_detection
from src.etl import run_etl
from src.warehouse import build_warehouse
from src.analytics import run_analytics

def main():
    start_time = time.time()
    print("="*50)
    print("Starting Traffic Analytics Pipeline")
    print("="*50)
    
    import src.config as config
    videos = list(config.RAW_DATA_DIR.rglob("*.mp4"))
    if not videos:
        print(f"No videos found in {config.RAW_DATA_DIR}")
        return
        
    for video_path in videos:
        print(f"\n{'*'*40}")
        print(f"PROCESSING VIDEO: {video_path.name}")
        print(f"{'*'*40}")
        
        print("\n>>> Phase 2: Vehicle Detection & Tracking")
        run_detection(video_path)
        
        print("\n>>> Phase 3 & 4: Traffic Aggregation & ETL")
        run_etl(video_path)
        
        print("\n>>> Phase 5: Data Warehouse Creation")
        build_warehouse()
        
    print("\n>>> Phase 6: SQL Analytics")
    run_analytics()
    
    elapsed_time = time.time() - start_time
    print("="*50)
    print(f"Pipeline completed successfully in {elapsed_time:.2f} seconds!")
    print("="*50)

if __name__ == "__main__":
    main()

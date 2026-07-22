import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Inputs & Outputs
DETECTIONS_CSV_PATH = PROCESSED_DATA_DIR / "vehicle_detections.csv"
TRAFFIC_PER_MINUTE_CSV_PATH = PROCESSED_DATA_DIR / "traffic_per_minute.csv"
POSTGRES_URI = os.getenv("POSTGRES_URI")
ANALYTICS_SQL_PATH = OUTPUTS_DIR / "analytics_results.sql"

# YOLO Config
YOLO_MODEL = "yolo11n.pt"  
CONFIDENCE_THRESHOLD = 0.3
TRACKER = "bytetrack.yaml"

# Video Metadata Mapping
CAMERAS = {
    "camera_01": {
        "camera_name": "Camera 01",
        "road": "Jl. Pandanaran",
        "city": "Semarang"
    },
    "camera_02": {
        "camera_name": "Camera 02",
        "road": "Tol Kaligawe",
        "city": "Semarang"
    },
    "camera_03": {
        "camera_name": "Camera 03",
        "road": "Simpang Lima",
        "city": "Semarang"
    }
}

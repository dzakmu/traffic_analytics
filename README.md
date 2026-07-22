# Traffic Analytics Pipeline

## Project Overview
This project implements a Traffic Analytics Pipeline that processes traffic video footage to detect and track vehicles, aggregates the traffic data, and loads it into a Data Warehouse (Star Schema in PostgreSQL) ready for analytics and Power BI dashboards.

## Architecture
The pipeline consists of the following components:
1. **Vehicle Detection (`src/vehicle_detection.py`)**: Uses YOLO11n and ByteTrack to detect and track vehicles in video.
2. **Traffic Aggregation (`src/etl.py`)**: Aggregates raw detections into traffic counts per minute.
3. **ETL Pipeline (`src/etl.py`)**: Extracts the aggregated data, transforms it by adding time/location dimensions, and loads it into a PostgreSQL Database.
4. **Data Warehouse (`src/warehouse.py`)**: A Star Schema implemented in PostgreSQL containing `fact_traffic`, `dim_time`, `dim_vehicle`, and `dim_camera`.
5. **Analytics (`src/analytics.py`)**: SQL queries to answer business questions (Peak hours, Vehicle types, etc.).

## Directory Structure
```
trafficanalytics/
├── data/
│   ├── processed/         # Intermediate CSV files containing detections
│   └── raw/               # Input traffic video (.mp4)
├── outputs/               # Annotated videos and analytics results (.sql)
├── src/
│   ├── analytics.py       # SQL Analytics scripts
│   ├── config.py          # Project configuration
│   ├── etl.py             # Extract, Transform, Load processes
│   ├── main.py            # Main pipeline script
│   ├── vehicle_detection.py # YOLO and ByteTrack logic
│   └── warehouse.py       # Data Warehouse creation logic
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Dataset
- **Input**: Traffic videos placed in `data/raw/` (e.g. `sample_traffic.mp4`)
- **Intermediate**: CSV files stored in `data/processed/`
- **Output**: 
  - PostgreSQL database (Supabase)
  - Annotated videos: `outputs/annotated_*.mp4`
  - Analytics results: `outputs/analytics_results.sql`

## Installation
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```
*(Key dependencies include: `ultralytics`, `opencv-python`, `pandas`, `sqlalchemy`, `psycopg2-binary`)*

2. Add your raw video files to `data/raw/`.

3. Run the complete pipeline:
```bash
python src/main.py
```

## Dashboard & Insights
The PostgreSQL database is connected to **Power BI** to create interactive dashboards based on the star schema. 

### Power BI Dashboard
*(TIPS: Letakkan screenshot dashboard Power BI Anda di folder `outputs/` atau `docs/`, lalu panggil gambarnya di sini. Contoh:)*
<!-- ![Power BI Dashboard](outputs/dashboard_screenshot.png) -->

### Key Insights
*(TIPS: Anda bisa menambahkan 3-4 poin temuan utama dari data analitik di sini)*
- **Peak Hours:** Waktu puncak volume kendaraan tertinggi terjadi pada pukul ...
- **Vehicle Types:** Mayoritas kendaraan yang melintas adalah jenis ... dengan persentase sebesar ...%
- **Busiest Camera/Road:** Lokasi dengan traffic tertinggi terpantau pada ...

## Future Improvement
- Real-time video stream processing.
- Advanced vehicle re-identification across multiple cameras.
- Deployment to other cloud data warehouses (e.g., Snowflake, Redshift, or BigQuery).

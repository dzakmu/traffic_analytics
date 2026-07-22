# Traffic Analytics Pipeline

An end-to-end **Computer Vision**, **Data Engineering**, and **Business Intelligence** project that detects and tracks vehicles from traffic videos using **YOLO11** and **ByteTrack**, transforms detection results through an automated **ETL Pipeline**, stores them in a **PostgreSQL Star Schema Data Warehouse**, and visualizes traffic insights using **Power BI**.

---

## Project Overview

This project demonstrates a complete analytics pipeline starting from raw traffic videos to interactive business dashboards.

The pipeline consists of:

- Vehicle Detection using YOLO11
- Multi-object Tracking using ByteTrack
- Traffic Aggregation
- ETL Pipeline
- PostgreSQL Data Warehouse
- SQL Analytics
- Interactive Power BI Dashboard

The objective is to demonstrate an end-to-end workflow commonly used in modern AI and Data Engineering projects.

---

# ⚠ Disclaimer

> **This project is intended for educational and portfolio purposes only.**

Although the vehicle detection pipeline is implemented using **YOLO11** and **ByteTrack**, the traffic aggregation, road names, camera locations, dashboard metrics, and analytical results are generated from **dummy/simulated data**.

The purpose of this project is to demonstrate technical implementation rather than represent actual traffic conditions.

---


#  System Architecture

```
Traffic Video
      │
      ▼
YOLO11 Vehicle Detection
      │
      ▼
ByteTrack Vehicle Tracking
      │
      ▼
Detection CSV
      │
      ▼
ETL Pipeline
      │
      ▼
PostgreSQL Data Warehouse
      │
      ▼
SQL Analytics
      │
      ▼
Power BI Dashboard
```

---

# Data Warehouse

The project implements a Star Schema consisting of one Fact Table and three Dimension Tables.

```
<img width="1140" height="713" alt="Data Model" src="https://github.com/user-attachments/assets/4cede0c4-6be7-4f8d-9afc-554f9c7fb027" />

<img width="1140" height="713" alt="Data Model" src="https://github.com/user-attachments/assets/e9d6b8a9-dd44-4a36-b3c3-48b84b5bd624" />


```

### Fact Table

- fact_traffic

### Dimension Tables

- dim_time
- dim_camera
- dim_vehicle

---

# Project Structure

```
trafficanalytics/
├── data/
│   ├── processed/
│   └── raw/
│
├── docs/
│   ├── Data Model.png
│   ├── Drill Trough Dashboard.png
│   ├── Main Dashboard.png
│
├── outputs/
│   ├── annotated_video.mp4
│   └── analytics_results.sql
│
├── src/
│   ├── analytics.py
│   ├── config.py
│   ├── etl.py
│   ├── main.py
│   ├── vehicle_detection.py
│   └── warehouse.py
│
├── requirements.txt
└── README.md
```

---

# Pipeline Components

## 1. Vehicle Detection

Detects vehicles from traffic videos using **YOLO11**.

Supported classes:

- Car
- Motorcycle
- Truck
- Bus

---

## 2. Vehicle Tracking

Tracks detected vehicles using **ByteTrack** to avoid duplicate counting.

---

## 3. Traffic Aggregation

Aggregates detection results into traffic counts.

Example:

| fact_id | time_id | vehicle_id | camera_id |vehicle_count |
|-------|----------|------------|-------|---------------|
|1|1|1|1|16|
|2|134|2|2|16|

---

## 4. ETL Pipeline

Transforms raw detections into dimensional data.

Creates:

- Time Dimension
- Camera Dimension
- Vehicle Dimension
- Fact Traffic

---

## 5. Data Warehouse

Loads transformed data into PostgreSQL.

Supports analytical queries efficiently through Star Schema.

---

## 6. Analytics

SQL queries answer business questions such as:

- What is the busiest road?
- What is the peak traffic hour?
- Which vehicle dominates the traffic?
- How does traffic change throughout the week?

---

# Power BI Dashboard

## Main Dashboard

```
<img width="1197" height="672" alt="Main Dashboard" src="https://github.com/user-attachments/assets/bfcc18f0-3c0b-4334-98d0-a586f6dffae4" />

```

Features:

- KPI Cards
- Interactive Filters
- Traffic Trend
- Vehicle Composition
- Traffic by Road
- Dynamic Tooltips
- Drillthrough Analysis

---

## Road Detail Dashboard

```
<img width="1203" height="677" alt="Drill Trough Dashboard" src="https://github.com/user-attachments/assets/7e5271a8-43fb-4b24-afcb-bf788d5fac98" />

```

Features

- Road-specific analysis
- Hourly trend
- Daily Trend
- Vehicle composition
- Raw transaction table

---

# Key Insights

> **The following insights are generated from dummy/simulated data and are intended to demonstrate analytical capabilities.**

### Peak Hour

Traffic volume reaches its highest point at **18:00**, indicating the evening rush hour.

---

### Dominant Vehicle

Motorcycles contribute approximately **60%** of the total traffic volume.

---

### Busiest Road

**Simpang Lima** records the highest traffic volume among all monitored locations.

---

### Weekly Trend

Traffic is consistently higher on weekdays than on weekends.

---

### Vehicle Composition

Passenger vehicles (Cars and Motorcycles) account for over **90%** of total detected vehicles.

---

# Business Questions

This dashboard helps answer questions such as:

- Which road experiences the highest traffic volume?
- What is the busiest hour of the day?
- Which vehicle type dominates traffic?
- How does traffic vary by weekday?
- Which camera records the most vehicles?

---

# Installation

Clone the repository

```bash
[git clone https://github.com/dzakmu/traffic_analytics.git]

cd traffic_analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Place traffic videos inside

```
data/raw/
```

Run the pipeline

```bash
python src/main.py
```

---

# Output

The pipeline generates:

```
Annotated Video

↓

Detection CSV

↓

PostgreSQL Database

↓

Power BI Dashboard
```

---

# Future Improvements

- Real-time video stream processing
- Apache Kafka integration
- Apache Airflow orchestration
- Docker deployment
- Cloud deployment
- Multi-camera tracking
- Automatic dashboard refresh
- GPS-enabled traffic mapping

---

# Author

**Muhammad Dzaky Mu'ammar**

Bachelor of Informatics

Diponegoro University

GitHub:
https://github.com/dzakmu

LinkedIn:
Muhammad Dzaky Mu'ammar

---


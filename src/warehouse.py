import psycopg2
import pandas as pd
import src.config as config

def build_warehouse():
    print("Building Data Warehouse (Star Schema in PostgreSQL)...")
    
    enriched_csv_path = config.PROCESSED_DATA_DIR / "enriched_traffic.csv"
    try:
        df = pd.read_csv(enriched_csv_path)
    except FileNotFoundError:
        print("Error: enriched data not found. Run ETL first.")
        return

    conn = psycopg2.connect(config.POSTGRES_URI)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_time (
        time_id SERIAL PRIMARY KEY,
        datetime TEXT UNIQUE,
        date TEXT,
        hour INTEGER,
        weekday TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_vehicle (
        vehicle_id SERIAL PRIMARY KEY,
        vehicle_type TEXT UNIQUE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_camera (
        camera_id SERIAL PRIMARY KEY,
        camera_name TEXT,
        road_name TEXT,
        city TEXT,
        UNIQUE(camera_name, road_name, city)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fact_traffic (
        fact_id SERIAL PRIMARY KEY,
        time_id INTEGER,
        vehicle_id INTEGER,
        camera_id INTEGER,
        vehicle_count INTEGER,
        FOREIGN KEY(time_id) REFERENCES dim_time(time_id),
        FOREIGN KEY(vehicle_id) REFERENCES dim_vehicle(vehicle_id),
        FOREIGN KEY(camera_id) REFERENCES dim_camera(camera_id)
    )
    ''')
    
    conn.commit()
    
    if df.empty:
        print("Enriched data is empty. Schema created but no data loaded.")
        conn.close()
        return

    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO dim_time (datetime, date, hour, weekday) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (datetime) DO NOTHING;
        ''', (row['datetime'], row['date'], row['hour'], row['weekday']))
        cursor.execute("SELECT time_id FROM dim_time WHERE datetime = %s;", (row['datetime'],))
        time_id = cursor.fetchone()[0]
  
        cursor.execute('''
            INSERT INTO dim_vehicle (vehicle_type) 
            VALUES (%s) 
            ON CONFLICT (vehicle_type) DO NOTHING;
        ''', (row['vehicle_type'],))
        cursor.execute("SELECT vehicle_id FROM dim_vehicle WHERE vehicle_type = %s;", (row['vehicle_type'],))
        vehicle_id = cursor.fetchone()[0]
     
        cursor.execute('''
            INSERT INTO dim_camera (camera_name, road_name, city) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (camera_name, road_name, city) DO NOTHING;
        ''', (row['camera'], row['road'], row['city']))
        cursor.execute("SELECT camera_id FROM dim_camera WHERE camera_name = %s AND road_name = %s AND city = %s;", 
                       (row['camera'], row['road'], row['city']))
        camera_id = cursor.fetchone()[0]

        cursor.execute('''
        INSERT INTO fact_traffic (time_id, vehicle_id, camera_id, vehicle_count)
        VALUES (%s, %s, %s, %s)
        ''', (time_id, vehicle_id, camera_id, row['vehicle_count']))
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data successfully loaded into PostgreSQL Data Warehouse!")

if __name__ == "__main__":
    build_warehouse()

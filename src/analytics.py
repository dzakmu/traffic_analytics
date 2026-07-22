import psycopg2
import pandas as pd
import src.config as config

def run_analytics():
    print("Running SQL Analytics on PostgreSQL Data Warehouse...")
    
    try:
        conn = psycopg2.connect(config.POSTGRES_URI)
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Please ensure the warehouse step has been executed.")
        return
        
    queries = {
        "Total Vehicle": '''
            SELECT SUM(vehicle_count) as total_vehicles
            FROM fact_traffic
        ''',
        "Vehicle Type": '''
            SELECT v.vehicle_type, SUM(f.vehicle_count) as total_vehicles
            FROM fact_traffic f
            JOIN dim_vehicle v ON f.vehicle_id = v.vehicle_id
            GROUP BY v.vehicle_type
            ORDER BY total_vehicles DESC
        ''',
        "Peak Hour": '''
            SELECT t.hour, SUM(f.vehicle_count) as total_vehicles
            FROM fact_traffic f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.hour
            ORDER BY total_vehicles DESC
        ''',
        "Camera Analysis": '''
            SELECT c.camera_name, c.road_name, c.city, SUM(f.vehicle_count) as total_vehicles
            FROM fact_traffic f
            JOIN dim_camera c ON f.camera_id = c.camera_id
            GROUP BY c.camera_name, c.road_name, c.city
            ORDER BY total_vehicles DESC
        ''',
        "Daily Trend": '''
            SELECT t.date, SUM(f.vehicle_count) as total_vehicles
            FROM fact_traffic f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.date
            ORDER BY t.date
        '''
    }
    
    with open(config.ANALYTICS_SQL_PATH, 'w') as sql_file:
        for name, query in queries.items():
            print(f"\n--- {name} ---")
            try:
                # read_sql_query supports psycopg2 connection
                df = pd.read_sql_query(query, conn)
                print(df.to_string(index=False))
            except pd.errors.DatabaseError as e:
                print(f"Error executing query: {e}")
            
            # Save query to .sql script
            sql_file.write(f"-- {name}\n")
            sql_file.write(f"{query.strip()};\n\n")
            
    conn.close()
    print(f"\nAnalytics completed. SQL script saved to {config.ANALYTICS_SQL_PATH}")

if __name__ == "__main__":
    run_analytics()

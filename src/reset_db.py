import psycopg2
import src.config as config

def reset_database():
    print("Connecting to PostgreSQL to reset database...")
    try:
        conn = psycopg2.connect(config.POSTGRES_URI)
        cursor = conn.cursor()
        
        cursor.execute('''
            TRUNCATE TABLE fact_traffic, dim_time, dim_vehicle, dim_camera RESTART IDENTITY CASCADE;
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database berhasil dikosongkan! Semua tabel sekarang bersih dan ID kembali dari 1.")
        
    except Exception as e:
        print(f"❌ Gagal mengosongkan database: {e}")

if __name__ == "__main__":
    print("⚠️ PERINGATAN: Aksi ini akan menghapus semua data analisis lalu lintas Anda dari database Supabase.")
    confirm = input("Apakah Anda yakin ingin mengosongkan database? (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Operasi dibatalkan.")

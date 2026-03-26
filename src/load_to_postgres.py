import os
import pandas as pd  # type: ignore
from sqlalchemy import create_engine  # type: ignore

# Thông tin kết nối lấy từ docker-compose.yml
DB_USER = "olist_user"
DB_PASSWORD = "olist_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist_db"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_dir = os.path.join(base_path, 'data', 'bronze')
    
    if not os.path.exists(bronze_dir):
        print(f"Thư mục {bronze_dir} không tồn tại. Hãy chắc chắn bạn đã chạy download_data.py trước.")
        return

    csv_files = [f for f in os.listdir(bronze_dir) if f.endswith('.csv')]
    if not csv_files:
        print("Không có file CSV nào trong thư mục data/bronze.")
        return
        
    print("Bắt đầu nạp dữ liệu từ Bronze (CSV) vào PostgreSQL...")
    for file in csv_files:
        table_name = file.replace('.csv', '')
        file_path = os.path.join(bronze_dir, file)
        
        print(f"Đang nạp file {file} vào bảng public.{table_name}...")
        
        # Đọc dữ liệu
        df = pd.read_csv(file_path)
        
        # Lưu vào PostgreSQL, mode 'replace'
        df.to_sql(name=table_name, con=engine, schema='public', if_exists='replace', index=False)
        print(f"✅ Đã nạp xong bảng {table_name}: {len(df)} dòng.")

if __name__ == "__main__":
    load_data()
    print("🎉 Hoàn tất nạp dữ liệu vào PostgreSQL. Bạn có thể lấy DBeaver connect vào localhost:5432 để kiểm tra.")

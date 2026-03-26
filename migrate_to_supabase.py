import pandas as pd  # type: ignore
from sqlalchemy import create_engine 
import os

# Thay thế bằng Connection URI của bạn trên Supabase (Project Settings -> Database)
# Đảm bảo connection string bắt đầu bằng postgresql:// thay vì postgres://
SUPABASE_URL = "postgresql://postgres.wijxfocmzmhceterprmz:PhamLoc090504%40@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
def push_data():
    if "BẬT_MẬT_KHAU_GIẤY_CỦA_BẠN" in SUPABASE_URL:
        print("❌ Cảnh báo: Bạn chưa cập nhật chuỗi kết nối SUPABASE_URL")
        return

    print("🔌 Đang kết nối đến Supabase...")
    engine = create_engine(SUPABASE_URL)
    
    # Đọc file parquet từ Gold Layer
    gold_path = "data/gold/kpi_by_state.parquet"
    if not os.path.exists(gold_path):
        print(f"❌ Không tìm thấy file dữ liệu tại {gold_path}. Vui lòng chạy ETL trước.")
        return
        
    print(f"📦 Đang đọc dữ liệu từ {gold_path}...")
    df = pd.read_parquet(gold_path)
    
    # Push Data lên bảng "gold_kpi_by_state" public schema
    print(f"🚀 Đang đưa {len(df)} dòng dữ liệu lên Supabase...")
    df.to_sql("gold_kpi_by_state", engine, schema="public", if_exists="replace", index=False)
    
    print("✅ Hoàn tất! Bảng 'gold_kpi_by_state' đã sẵn có trên Supabase.")

if __name__ == "__main__":
    push_data()

import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import os
import argparse



def run_etl():
    # Thư mục gốc tương đối so với vị trí chạy script
    # Nếu chạy script này trong Olist_Logistics_Project/notebooks/
    
    # Xác định đường dẫn tương đối
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_dir = os.path.join(base_path, 'data', 'bronze')
    silver_dir = os.path.join(base_path, 'data', 'silver')
    gold_dir = os.path.join(base_path, 'data', 'gold')
    
    # Kiểm tra dữ liệu Bronze
    orders_path = os.path.join(bronze_dir, 'olist_orders_dataset.csv')
    if not os.path.exists(orders_path):
        raise FileNotFoundError("Không tìm thấy bộ dữ liệu Olist trong Bronze layer. Hãy chạy download_data.py trước!")
    print("===== BẮT ĐẦU QUÁ TRÌNH ETL =====")
    
    print("1. Đọc dữ liệu từ Bronze Layer...")
    orders = pd.read_csv(os.path.join(bronze_dir, 'olist_orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(bronze_dir, 'olist_order_items_dataset.csv'))
    customers = pd.read_csv(os.path.join(bronze_dir, 'olist_customers_dataset.csv'))
    sellers = pd.read_csv(os.path.join(bronze_dir, 'olist_sellers_dataset.csv'))
    
    print("2. Tích hợp dữ liệu (Data Merging)...")
    # Merge Orders và Order Items
    df_merged = orders.merge(order_items, on='order_id', how='inner')
    # Merge với Customers
    df_merged = df_merged.merge(customers, on='customer_id', how='inner')
    # Merge với Sellers
    df_merged = df_merged.merge(sellers, on='seller_id', how='inner')
    
    print("3. Làm sạch và Feature Engineering...")
    # Lọc các đơn hàng đã giao (delivered)
    df_delivered = df_merged[df_merged['order_status'] == 'delivered'].copy()
    
    # Chuyển đổi định dạng ngày tháng
    date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        df_delivered[col] = pd.to_datetime(df_delivered[col])
        
    # Xoá dòng thiếu ngày giao hàng
    df_delivered.dropna(subset=['order_delivered_customer_date'], inplace=True)
    
    # Tính delivery_time (ngày giao thực tế - ngày đặt hàng)
    df_delivered['delivery_time_days'] = (df_delivered['order_delivered_customer_date'] - df_delivered['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
    
    # Tính estimated_error (ngày giao thực tế - ngày dự kiến)
    df_delivered['estimated_error_days'] = (df_delivered['order_delivered_customer_date'] - df_delivered['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)
    
    # Biến phân loại is_late (1 nếu trễ, 0 nếu đúng hạn)
    df_delivered['is_late'] = (df_delivered['estimated_error_days'] > 0).astype(int)
    
    print("4. Lưu dữ liệu sạch vào Silver Layer (.parquet)...")
    # Đảm bảo thư mục tồn tại
    os.makedirs(silver_dir, exist_ok=True)
    silver_path = os.path.join(silver_dir, 'master_logistics.parquet')
    df_delivered.to_parquet(silver_path, index=False)
    print(f"[{silver_path}] đã được lưu.")
    
    print("5. Aggregate Insights và Lưu vào Gold Layer...")
    os.makedirs(gold_dir, exist_ok=True)
    
    # KPI 1: Phân tích địa lý - Thời gian giao hàng và Tỷ lệ OTD theo Bang (State của Customer)
    state_kpi = df_delivered.groupby('customer_state').agg(
        total_orders=('order_id', 'nunique'),
        late_orders=('is_late', 'sum'),
        avg_delivery_time=('delivery_time_days', 'mean'),
        avg_freight_value=('freight_value', 'mean')
    ).reset_index()
    
    # Tính OTD (On-Time Delivery Rate) = (Total - Late) / Total
    state_kpi['ontime_delivery_rate'] = ((state_kpi['total_orders'] - state_kpi['late_orders']) / state_kpi['total_orders']) * 100
    
    # Lưu xuống Gold Layer
    gold_kpi_path = os.path.join(gold_dir, 'kpi_by_state.parquet')
    state_kpi.to_parquet(gold_kpi_path, index=False)
    print(f"[{gold_kpi_path}] đã được lưu.")
    
    print("===== HOÀN TẤT QUÁ TRÌNH ETL =====")
    print("Dữ liệu đã sẵn sàng cho Giao diện Dashboard (Streamlit).")

if __name__ == "__main__":
    run_etl()

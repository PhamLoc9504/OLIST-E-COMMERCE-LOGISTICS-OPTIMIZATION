# 🚚 Olist E-Commerce Logistics Optimization Dashboard

![Dashboard Preview](assets/dashboard.png)

Logistics Automation & Data Pipeline Project for Brazilian E-commerce dataset (Olist). This project processes and analyzes historical delivery and order data to identify operational bottlenecks and visualize logistics efficiency across Brazil.

## 🛠️ Tech Stack & Tools (Dùng "cái gì gì" và "đồ các kiểu")

*   **Programming Language:** Python 3 (Pandas, PyArrow, NumPy) - Thực hiện xử lý ETL logic, tính toán các Feature quan trọng.
*   **Data Warehouse (Storage):** PostgreSQL (Containerized) - Lưu trữ Gold layer KPI thay đổi linh hoạt, đáp ứng khả năng query tốc độ cao.
*   **Data Transformation:** dbt (Data Build Tool) - Chịu trách nhiệm thiết lập các mô hình dữ liệu, transform dữ liệu từ Silver sáng Gold-layer KPI chuẩn kiến trúc.
*   **Infrastructure & Deployment:** Docker & Docker Compose - Đóng gói toàn bộ Database và môi trường lên Cloud/Local cực nhanh chỉ bằng 1 câu lệnh.
*   **Data Visualization (Dashboard):** Streamlit & Plotly (Tích hợp custom HTML/JS/CSS) - Giải pháp dựng web apps ngay trên Python, inject code JS để tạo bản đồ Geospatial có tương tác.

## 🏗️ Kiến Trúc Dữ Liệu (Medallion Architecture)
Dự án được xây dựng luồng dữ liệu theo chuẩn công nghiệp (Bronze - Silver - Gold):
1.  **Bronze Layer (Raw):** Dữ liệu thô (CSV) được load trực tiếp qua API từ Kaggle (Olist Public Dataset).
2.  **Silver Layer (Cleaned & Featurized):** 
    *   Thực hiện làm sạch cơ bản (Clean nulls) và Join các bảng (`Orders`, `Items`, `Customers`) bằng script Python/Jupyter Notebook.
    *   Tạo thêm Feature quan trọng: Tính toán `delivery_time_days` (bước chuyển trạng thái), cắm cờ `is_late` v.v.
    *   Lưu xuống local dưới định dạng **Parquet** (`fastparquet/pyarrow`) nhằm giảm dung lượng và tăng tốc I/O gấp nhiều lần CSV.
3.  **Gold Layer (Aggregated):** 
    *   Tập dữ liệu ở Silver được tổng hợp (Group by State/Region) và đưa vào các bảng phục vụ Dashboard thông qua **dbt models**.
    *   Lưu trữ trực tiếp trên **PostgreSQL Database** chạy trong Docker.
4.  **Presentation Layer:** 
    *   Ứng dụng `Streamlit` kết nối thẳng vào database PostgreSQL (`SQLAlchemy`) thông qua credentials nội bộ.
    *   Đổ dữ liệu lên giao diện bản đồ, đồ thị...

## 🚀 Hướng Dẫn Chạy (Quick Start)

### 1. Chuẩn bị Môi trường
```bash
# Tạo môi trường ảo (Khuyên dùng)
python -m venv venv
venv\Scripts\activate   # Trên Windows

# Cài đặt thư viện cần thiết
pip install -r requirements.txt
```

### 2. Khởi tạo Database (PostgreSQL qua Docker)
Đảm bảo bạn đã cài đặt Docker Desktop và đang chạy trương trình.
```bash
# Khởi động PostgreSQL ở background port 5432
docker-compose up -d
```

### 3. Chạy Pipeline ETL & dbt (Tùy chọn)
Chạy notebook hoặc script ETL bên trong thư mục `notebooks` để nhào nặn dữ liệu rồi bắn vào Postgres. Nếu bạn đã có Postgres được load sẵn data, có thể bỏ qua.
```bash
dbt run --profiles-dir ./olist_dbt
```

### 4. Bật Dashboard Streamlit
```bash
streamlit run src/main.py
```
Sau đó truy cập vào trình duyệt cung cấp (thường là `http://localhost:8501`).

## 📊 Tính Năng Của Dashboard
*   **Geospatial Interaction:** Bản đồ tương tác sử dụng HTML/JS tùy chỉnh, biểu thị thông số vận chuyển từng bang.
*   **Real-time querying:** Dữ liệu hoàn toàn đọc từ source DB với kết nối SQLAlchemy.
*   **Core KPIs tracked:** On-time Delivery Rate (OTD), Thời gian giao hàng trung bình, Tổng lượng đơn, Cước vận chuyển.

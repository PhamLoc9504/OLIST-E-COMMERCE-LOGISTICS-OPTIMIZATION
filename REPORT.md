# BÁO CÁO DỰ ÁN TỐI ƯU VẬN HÀNH LOGISTICS - OLIST E-COMMERCE

## 1. GIỚI THIỆU BÀI TOÁN VÀ LÝ DO CHỌN ĐỀ TÀI
Logistics được xem là "xương sống" của ngành E-commerce đương đại. Tại thị trường rộng lớn và phức tạp như Brazil (nơi nền tảng thương mại điện tử Olist hoạt động), sự phân hóa về mặt địa lý tác động cực kỳ rõ rệt lên chi phí và thời gian giao hàng. Những khu vực trọng điểm như Sao Paulo có lợi thế về hạ tầng, trong khi các bang xa xôi gặp bất lợi lớn.
Việc tối ưu giao nhận không chỉ đóng vai trò nâng cao trải nghiệm khách hàng (Customer Experience), mà còn là bài toán sống còn để tối ưu hóa tỷ suất lợi nhuận. Đề tài này nhằm mục tiêu phân tích các chỉ số KPI vận hành, mô phỏng cách dữ liệu thô (raw data) được biến đổi thành các Insight giá trị, qua đó giúp doanh nghiệp xác định các nút thắt (bottlenecks) và ra quyết định chiến lược.

## 2. NGUỒN DỮ LIỆU SỬ DỤNG
Dự án sử dụng bộ dữ liệu thực tế **Brazilian E-Commerce Public Dataset by Olist** được công bố chính thức trên Kaggle.
- **Tính hợp lệ:** Nguồn gốc rõ ràng, dữ liệu mở phục vụ mục đích học thuật và nghiên cứu.
- **Thành phần dữ liệu:** Sử dụng 4 bảng dữ liệu cốt lõi gồm:
  1. `olist_orders_dataset.csv`: Thông tin tổng quan về đơn hàng (ID, trạng thái, thời gian đặt/giao).
  2. `olist_order_items_dataset.csv`: Chi tiết mỗi đơn hàng (mã sản phẩm, mã người bán, chi phí vận chuyển - freight value).
  3. `olist_customers_dataset.csv`: Vị trí địa lý (thành phố, bang) của người mua.
  4. `olist_sellers_dataset.csv`: Vị trí địa lý của người bán.

## 3. QUY TRÌNH THỰC HIỆN VÀ KIẾN TRÚC DỮ LIỆU
Dự án thực hiện đầy đủ luồng ETL (Extract - Transform - Load) theo mô hình **Medallion Architecture**:

- **Thu thập dữ liệu (Bronze Layer):** 
  Dữ liệu được tải trực tiếp từ Kaggle Hub thông qua API và lưu trữ ở dạng CSV gốc, giữ nguyên trạng thái chưa chỉnh sửa.
  
- **Làm sạch và Kỹ thuật đặc trưng (Silver Layer):** 
  Thực hiện Data Merging (Tích hợp dữ liệu qua các khóa ngoại `order_id`, `customer_id`, `seller_id`). Gạt bỏ các đơn hàng bị hủy hoặc không có ngày giao hàng. Tạo thêm các cột (Feature Engineering) như `delivery_time_days` (thời gian giao hàng thực tế) và biến phân loại `is_late` (xác định đơn hàng trễ hẹn so với cam kết). Lưu dưới định dạng `.parquet` để nén và tăng tốc đọc/ghi.

- **Mô hình hóa / Tổng hợp KPI (Gold Layer):** 
  Dữ liệu được tổng hợp (Aggregated) theo cấu trúc không gian (Bảng `customer_state`) để tính toán các KPI: Số lượng đơn hàng, Tỷ lệ giao hàng đúng hạn (OTD%), Chi phí vận chuyển trung bình, Thời gian giao hàng trung bình.

## 4. KẾT QUẢ VÀ TRỰC QUAN HÓA (DASHBOARD)
Kết quả của lớp Gold được đưa vào **Streamlit Dashboard** để phân tích trực quan:
1. **Phân bố tỷ lệ đúng hạn (OTD) và Khối lượng đơn hàng:** Các bang vùng trung tâm kinh tế (như SP - Sao Paulo) thống trị về lượng đơn hàng, đồng thời duy trì tỷ lệ đúng hạn (OTD) ở mức rất cao.
2. **Nghịch lý chi phí và thời gian:** Ở khu vực các bang vùng sâu, phí vận chuyển (Freight Value) không những cao nhất mà tốc độ giao hàng cũng chậm nhất, tạo ra gánh nặng kép cho khách hàng.
3. **Mối quan hệ Tuyến tính:** Biểu đồ phân tán (Scatter Plot) trên Dashboard cho thấy tốc độ giao hàng chịu ảnh hưởng tuyến tính bởi phí vận chuyển. Nút thắt (Bottleneck) chủ yếu xảy ra do sự cách trở địa lý thay vì giới hạn nguồn hàng từ người bán.

## 5. NHẬN XÉT VÀ ĐỀ XUẤT GIẢI PHÁP
- **Quy hoạch kho bãi trung chuyển (Fulfillment Centers):** Olist nên mở rộng hoặc hợp tác với các kho vệ tinh (mini-warehouses) tại các cụm bang có lượng đơn đặt hàng tiềm năng nhưng thời gian giao lâu (nhằm giảm thiểu Bottleneck ở khâu Last-mile delivery).
- **Chính sách trợ giá (Subsidized Shipping):** Thiết kế điểm hòa vốn để trợ phí vận chuyển dựa trên khoảng cách địa lý, nhằm kích cầu tiêu dùng ở khu vực thưa dân, bù đắp thiệt thòi cho người mua ở ngoại vùng.
- **Theo dõi Carrier SLA:** Tăng cường đánh giá các đối tác vận chuyển thứ ba (3PLs) theo KPI từng khu vực.

## 6. HẠN CHẾ CỦA DỰ ÁN VÀ HƯỚNG PHÁT TRIỂN
**Hạn chế:**
- Dataset chỉ có các mốc thời gian vĩ mô (ngày đặt, ngày giao), thiếu dữ liệu cực nhỏ gọn (như thời gian lưu kho ở trạm trung chuyển, thời gian kẹt tắc đường) để có thể xác định chính xác nút thắt.
- Việc tính trung bình (Mean) cho phí vận chuyển và ngày giao hàng có thể bị ảnh hưởng bởi các giá trị ngoại lai (Outliers) của những đơn hàng siêu nặng hoặc cực kỳ xa.

**Hướng phát triển:**
- Ứng dụng mô hình Học máy (Machine Learning - Regression) để dự đoán số ngày giao hàng dự kiến (Estimated Delivery Date) một cách biến động theo thời gian thực thay vì fix tĩnh như hệ thống hiện hành của Olist.
- Phân tích Cluster (Gom cụm) địa lý để tự động tìm ra vị trí tối ưu để xây dựng kho vệ tinh.
- Triển khai Data Pipeline chạy tự động (Airflow / Mage.AI) thay vì thao tác script thủ công 1 chiều để theo dõi luồng data cập nhật theo ngày.

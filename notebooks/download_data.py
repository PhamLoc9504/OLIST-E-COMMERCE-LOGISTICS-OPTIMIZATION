import kagglehub  # type: ignore
import shutil
import os

print("Đang tải dataset thật từ Kaggle...")
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
print("Đường dẫn lưu tạm:", path)

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_dir = os.path.join(base_path, 'data', 'bronze')
os.makedirs(target_dir, exist_ok=True)

print(f"Đang copy dữ liệu vào {target_dir}...")
count: int = 0
for file in os.listdir(path):
    if file.endswith('.csv'):
        shutil.copy(os.path.join(path, file), os.path.join(target_dir, file))
        count += 1  # type: ignore
        
print(f"Thành công! Đã chuyển {count} file CSV vào thư mục Bronze.")

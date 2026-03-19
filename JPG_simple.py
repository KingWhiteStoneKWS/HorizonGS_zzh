import os
import shutil

# 原始图片文件夹
src_folder = "data/UAVScene_test/images"

# 新文件夹
dst_folder = "data/UAVScene_test/images_5"

os.makedirs(dst_folder, exist_ok=True)

# 获取所有jpg文件并排序
files = sorted([f for f in os.listdir(src_folder) if f.endswith(".jpg")])

# 每隔5张取一张
sampled_files = files[::5]

for file in sampled_files:
    src_path = os.path.join(src_folder, file)
    dst_path = os.path.join(dst_folder, file)
    shutil.copy(src_path, dst_path)

print(f"复制完成，共复制 {len(sampled_files)} 张图片")
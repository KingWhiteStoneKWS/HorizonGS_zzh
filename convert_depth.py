import os
import numpy as np
import cv2
import struct

# 设置路径
input_dir = "./data/my_scene/dense/stereo/depth_maps/aerial"
output_dir = "./data/my_scene/depths/aerial" # 你想要的 output 文件夹
os.makedirs(output_dir, exist_ok=True)

print("document ready")

def read_array(path):
    with open(path, "rb") as fid:
        width, height, channels = np.genfromtxt(fid, delimiter="&", max_rows=1, usecols=(0, 1, 2), dtype=int)
        fid.seek(0)
        num_delimiter = 0
        byte = fid.read(1)
        while True:
            if byte == b"&":
                num_delimiter += 1
                if num_delimiter >= 3:
                    break
            byte = fid.read(1)
        array = np.fromfile(fid, np.float32)
    array = array.reshape((width, height, channels), order="F")
    return np.transpose(array, (1, 0, 2)).squeeze()

for filename in os.listdir(input_dir):
    # 只处理 geometric (几何一致性) 的深度图
    if filename.endswith(".geometric.bin"):
        file_path = os.path.join(input_dir, filename)
        
        # 读取深度数据 (Metric Depth，单位通常是场景单位)
        depth = read_array(file_path)
        
        # 对应的原始图片名
        image_name = filename.replace(".geometric.bin", "")
        
        # -------------------------------------------------
        # 方式 1: 保存为 .npy (保留浮点精度，推荐给训练代码用)
        # -------------------------------------------------
        # np.save(os.path.join(output_dir, image_name + ".npy"), depth)
        
        # -------------------------------------------------
        # 方式 2: 保存为 .png (仅用于可视化，会丢失精度)
        # -------------------------------------------------
        # 简单的归一化可视化
        min_depth, max_depth = np.percentile(depth, [5, 95])
        depth[depth < min_depth] = min_depth
        depth[depth > max_depth] = max_depth
        depth_normalized = (depth - min_depth) / (max_depth - min_depth) * 255.0
        cv2.imwrite(os.path.join(output_dir, image_name + ".png"), depth_normalized.astype(np.uint8))

        print(f"Processed: {image_name}")
import os
import struct
import numpy as np

# --- 辅助函数：用于读取二进制数据 ---
def read_next_bytes(fid, num_bytes, format_char_sequence, endian_character="<"):
    data = fid.read(num_bytes)
    return struct.unpack(endian_character + format_char_sequence, data)

def qvec2rotmat(qvec):
    """将四元数转换为旋转矩阵"""
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

def inspect_images_bin(path_to_model):
    images_bin_path = os.path.join(path_to_model, "images.bin")
    
    print(f"正在尝试读取文件: {images_bin_path}")
    
    if not os.path.exists(images_bin_path):
        print(f"错误: 文件不存在! 请检查路径。")
        # 尝试检查是否有 txt 版本
        images_txt_path = os.path.join(path_to_model, "images.txt")
        if os.path.exists(images_txt_path):
            print(f" 发现 images.txt，但代码默认可能在寻找 .bin。请确认你的环境设置。")
        return

    images = {}
    
    try:
        with open(images_bin_path, "rb") as fid:
            num_reg_images = read_next_bytes(fid, 8, "Q")[0]
            print(f" 文件头读取成功。包含注册图像数量: {num_reg_images}")

            if num_reg_images == 0:
                print(" 警告: images.bin 中显示的图像数量为 0！Colmap 重建可能失败了。")
                return

            # 读取前 5 张图片作为示例
            for i in range(min(5, num_reg_images)): 
                binary_image_id = read_next_bytes(fid, 4, "i")[0]
                qvec = read_next_bytes(fid, 32, "dddd")
                tvec = read_next_bytes(fid, 24, "ddd")
                camera_id = read_next_bytes(fid, 4, "i")[0]
                
                image_name = ""
                current_char = read_next_bytes(fid, 1, "c")[0]
                while current_char != b"\x00":   # 读取文件名直到遇到 null 字符
                    image_name += current_char.decode("utf-8")
                    current_char = read_next_bytes(fid, 1, "c")[0]
                
                num_points2D = read_next_bytes(fid, 8, "Q")[0]
                # 跳过 2D 点数据，只读取文件头
                fid.seek(num_points2D * (24), 1) 

                # 计算相机中心 (模拟 dataset_readers.py 的逻辑)
                R = qvec2rotmat(qvec)
                t = np.array(tvec)
                W2C = np.zeros((4, 4))
                W2C[:3, :3] = R
                W2C[:3, 3] = t
                W2C[3, 3] = 1.0
                
                # 求逆得到 C2W，提取中心
                C2W = np.linalg.inv(W2C)
                cam_center = C2W[:3, 3]

                print(f"--- 图片 {i+1} ---")
                print(f"  ID: {binary_image_id}, Name: {image_name}")
                print(f"  Camera ID: {camera_id}")
                print(f"  计算出的 Center: {cam_center}")

    except Exception as e:
        print(f" 读取过程中发生错误: {e}")

# ==========================================
# 👇 请在这里修改为你的 sparse/0 文件夹的绝对路径
# 例如: "/home/zzh/data/my_scene/sparse/0"
dataset_sparse_path = "data/UAVScene_test/sparse/0" 
# ==========================================

if __name__ == "__main__":
    inspect_images_bin(dataset_sparse_path)
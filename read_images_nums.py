import os

# 定义路径，请根据你的实际路径修改
model_path = "data/eng_nor/sparse/0/images.bin"

def count_images(path):
    with open(path, "rb") as f:
        # COLMAP images.bin 的前 8 个字节是存储的图像数量 (uint64)
        import struct
        num_images = struct.unpack("<Q", f.read(8))[0]
        return num_images

try:
    count = count_images(model_path)
    print(f"✅ 成功注册（Registered）的图片数量为: {count}")
except Exception as e:
    print(f"❌ 读取失败: {e}")

#print("11")
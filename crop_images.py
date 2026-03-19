# file: crop_images.py

import os
from PIL import Image

def crop_bottom_272(input_dir: str, output_dir: str) -> None:
    """裁剪目录下所有 JPG 图片底部 272 像素并保存到 output_dir。"""
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".jpg", ".jpeg")):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        try:
            with Image.open(input_path) as img:
                width, height = img.size
                if height <= 272:
                    print(f"跳过 {filename}，高度不足 272px")
                    continue

                cropped = img.crop((0, 0, width, height - 272))
                cropped.save(output_path, quality=95)
                print(f"已处理: {filename}")
        except Exception as e:
            print(f"处理 {filename} 出错: {e}")


if __name__ == "__main__":
    # 示例：修改成你的实际路径
    input_dir = "./data/JingKou_community/251218/street_6_s2e"
    output_dir = "./data/JingKou_community/251218/street_6_s2e_crop"
    crop_bottom_272(input_dir, output_dir)

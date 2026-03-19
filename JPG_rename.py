import os
import argparse

def batch_rename_jpg(folder_path, prefix="aerial_", start_num=1, num_digits=4):
    """
    批量重命名指定文件夹中的JPG文件
    
    参数:
    folder_path: 存放JPG文件的文件夹路径
    prefix: 文件名前缀，默认是"aerial_"
    start_num: 起始编号，默认从1开始
    num_digits: 编号的位数，默认4位（0001、0002...）
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在！")
        return
    
    # 检查文件夹是否可访问
    if not os.path.isdir(folder_path):
        print(f"错误：'{folder_path}' 不是有效的文件夹路径！")
        return
    
    # 获取文件夹中所有JPG文件（区分大小写，同时匹配.jpg和.JPG）
    jpg_files = []
    for file_name in os.listdir(folder_path):
        # 获取文件完整路径
        file_path = os.path.join(folder_path, file_name)
        # 跳过文件夹，只处理文件
        if os.path.isfile(file_path):
            # 匹配所有JPG格式（.jpg/.JPG/.jpeg/.JPEG）
            if file_name.lower().endswith(('.jpg', '.jpeg')):
                jpg_files.append(file_path)
    
    # 如果没有找到JPG文件
    if not jpg_files:
        print("未在指定文件夹中找到JPG/JPEG文件！")
        return
    
    # 按文件创建时间排序（可选：也可以按名称排序，取消下面注释即可）
    # jpg_files.sort(key=lambda x: os.path.basename(x))
    jpg_files.sort(key=lambda x: os.path.getctime(x))
    
    # 批量重命名
    renamed_count = 0
    for idx, old_path in enumerate(jpg_files, start=start_num):
        # 生成新文件名：前缀 + 补零的编号 + .jpg
        new_name = f"{prefix}{idx:0{num_digits}d}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        # 处理重名情况
        if os.path.exists(new_path):
            print(f"警告：文件 '{new_name}' 已存在，跳过该文件")
            continue
        
        # 执行重命名
        try:
            os.rename(old_path, new_path)
            print(f"成功：{os.path.basename(old_path)} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"错误：重命名 {os.path.basename(old_path)} 失败 - {str(e)}")
    
    # 输出总结
    print(f"\n重命名完成！共处理 {len(jpg_files)} 个JPG文件，成功重命名 {renamed_count} 个")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='批量重命名JPG文件')
    parser.add_argument('folder', help='存放JPG文件的文件夹路径（绝对路径或相对路径）')
    parser.add_argument('--prefix', default='aerial_', help='文件名前缀，默认：aerial_')
    parser.add_argument('--start', type=int, default=1, help='起始编号，默认：1')
    parser.add_argument('--digits', type=int, default=4, help='编号位数，默认：4')
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行批量重命名
    batch_rename_jpg(
        folder_path=args.folder,
        prefix=args.prefix,
        start_num=args.start,
        num_digits=args.digits
    )

    #python JPG_rename.py data/260122
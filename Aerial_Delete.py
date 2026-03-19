import os
import glob
import shutil

def filter_photos(folder_path, keep_interval=5, dry_run=True):
    """
    按间隔保留照片，删除其余照片
    :param folder_path: 照片文件夹路径
    :param keep_interval: 保留间隔（隔5张留1张即设为5）
    :param dry_run: 干运行模式（True=只预览，False=实际删除）
    """
    # 校验文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在！")
        return

    # 定义要处理的图片格式（可根据需要添加）
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
    # 获取所有图片文件，按文件名排序
    photo_files = [
        f for f in glob.glob(os.path.join(folder_path, '*'))
        if os.path.isfile(f) and f.lower().endswith(image_extensions)
    ]
    # 按文件名排序（确保顺序正确）
    photo_files.sort()

    # 校验是否有图片文件
    if not photo_files:
        print("错误：文件夹中未找到图片文件！")
        return

    # 计算要保留和删除的文件
    keep_files = photo_files[::keep_interval]  # 隔5张取1张（索引0,5,10...）
    delete_files = [f for f in photo_files if f not in keep_files]

    # 输出预览信息
    print(f"===== 筛选结果预览 =====")
    print(f"文件夹中共有 {len(photo_files)} 张图片")
    print(f"计划保留 {len(keep_files)} 张，删除 {len(delete_files)} 张")
    print(f"\n保留的文件示例（前5个）：")
    for f in keep_files[:5]:
        print(f"  - {os.path.basename(f)}")
    print(f"\n删除的文件示例（前5个）：")
    for f in delete_files[:5]:
        print(f"  - {os.path.basename(f)}")

    # 实际执行删除（仅当dry_run=False时）
    if not dry_run:
        print(f"\n===== 开始删除文件 =====")
        deleted_count = 0
        for f in delete_files:
            try:
                os.remove(f)
                deleted_count += 1
                print(f"已删除：{os.path.basename(f)}")
            except Exception as e:
                print(f"删除失败 {os.path.basename(f)}：{e}")
        print(f"\n删除完成！共删除 {deleted_count} 个文件，剩余 {len(keep_files)} 个文件")
    else:
        print(f"\n===== 干运行模式 =====")
        print("未实际删除任何文件！如需执行删除，请将 dry_run 参数改为 False。")

if __name__ == "__main__":
    # ====================== 配置参数 ======================
    # 替换为你的照片文件夹路径（绝对路径/相对路径均可）
    PHOTO_FOLDER = "/home/zzh/HorizonGS/data/eng_nor_x/images/aerial"  # Linux/macOS示例
    # PHOTO_FOLDER = r"C:\HorizonGS\data\JingKou_community\photos"  # Windows示例（r避免转义）
    KEEP_INTERVAL = 10  # 隔5张留1张
    DRY_RUN = False     # 先设为True预览，确认后改为False执行删除
    # =====================================================

    # 执行筛选
    filter_photos(PHOTO_FOLDER, KEEP_INTERVAL, DRY_RUN) 
"""Print an ASCII Snek.

Usage:
    将脚手架拷贝到工程目录
    loran [--dir="E:\your_project_dir"]

"""
import os
import shutil
import fire  #用来编写命令行的,主要适用于子命令场景


def copy_files(src_folder, dst_folder):
    # 检查源文件夹是否存在
    if not os.path.exists(src_folder):
        print(f"源文件夹 {src_folder} 不存在。")
        return

    # 如果目标文件夹不存在，则创建它
    print("准备拷贝文件")
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"目标文件夹 {dst_folder} 已创建。")

    # 遍历源文件夹中的所有文件和子目录
    for item in os.listdir(src_folder):
        src_item = os.path.join(src_folder, item)
        dst_item = os.path.join(dst_folder, item)

        if os.path.isdir(src_item):
            # 如果是目录，递归拷贝
            shutil.copytree(src_item, dst_item)
            print(f"已拷贝目录 {src_item} 到 {dst_item}")
        else:
            # 如果是文件，直接拷贝
            shutil.copy2(src_item, dst_item)
            print(f"已拷贝文件 {src_item} 到 {dst_item}")
    print("文件拷贝结束")

def copy_scaf_dir_to_prj_dir(prj_dir):
    # 获取当前文件的完整路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件所在的文件夹路径
    current_folder_path = os.path.dirname(current_file_path)
    # 当前目录

    scaffold_path = os.path.join(current_folder_path, "scaffold")
    print("脚手架文件目录", scaffold_path)

    destination_path = prj_dir  # 确保目标文件夹路径正确
    print("destination_path", destination_path)

    copy_files(scaffold_path, destination_path)



class Loran:
    def init(self, prj_dir):
        """初始化工程"""
        print("正在初始化工程... \n")
        copy_scaf_dir_to_prj_dir(prj_dir)
        print("cases 目录和files目录下的 __init__.py文件 可以移除\n")
        print("初始化工程完成! 恭喜你, 即将踏入奇妙的自动化测试之旅")


def main():
    """Loran 命令行工具的入口"""
    fire.Fire(Loran)



if __name__ == "__main__":
    main()

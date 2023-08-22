import os
import sys


def change_extension(filename, new_extension):
    base_name = os.path.splitext(filename)[0]
    new_filename = f"{base_name}.{new_extension}"
    return new_filename


def batch_change_extension(folder_path, new_extension):
    count = 0
    for folder_name, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            if not filename.endswith(new_extension):
                file_path = os.path.join(folder_name, filename)
                new_filename = change_extension(filename, new_extension)
                new_file_path = os.path.join(folder_name, new_filename)
                os.rename(file_path, new_file_path)
                count += 1
    return count


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python change_extension.py <文件夹路径> <新扩展名>")
        sys.exit(1)

    source_folder = sys.argv[1]
    new_extension = sys.argv[2]

    modified_count = batch_change_extension(source_folder, new_extension)
    print(f"已修改 {modified_count} 个文件的扩展名为 {new_extension}")

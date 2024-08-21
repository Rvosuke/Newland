import os
import shutil

def delete_checkpoints(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            if name == '.checkpoints' or '.checkpoint':
                checkpoint_path = os.path.join(root, name)
                try:
                    shutil.rmtree(checkpoint_path)
                    print(f"Deleted: {checkpoint_path}") 
                except Exception as e:
                    print(f"Error deleting {checkpoint_path}: {e}")

if __name__ == "__main__":
    target_directory = './'
    if os.path.isdir(target_directory):
        delete_checkpoints(target_directory)
        print("清理完成。")
    else:
        print("输入的路径不是有效的目录。")
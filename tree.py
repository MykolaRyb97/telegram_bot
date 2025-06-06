import os
from pathlib import Path

def print_directory_tree(directory, prefix=""):
    items = sorted(os.listdir(directory))
    for index, item in enumerate(items):
        full_path = Path(directory) / item
        is_last = index == len(items) - 1
        new_prefix = prefix + ("└── " if is_last else "├── ")

        print(f"{new_prefix}{item}")

        if os.path.isdir(full_path):
            child_prefix = prefix + ("    " if is_last else "│   ")
            print_directory_tree(full_path, child_prefix)

project_root = "C:/Users/User/Desktop/telegram_bot"
print_directory_tree(project_root)



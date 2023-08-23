import sys
import pathlib

def get_root_folder(path, root_folder):
    for parent_folder in pathlib.Path(__file__).parents:
        if parent_folder.name == root_folder:
            return parent_folder
    raise FileNotFoundError(f"Root Folder {root_folder} not in path {path}")

def add_root_to_path(path, root_folder):
    root = get_root_folder(path, root_folder)
    sys.path.append(str(root))
    return root

ROOT_FOLDER = [str(folder) for folder in pathlib.Path(__file__).parents if folder.name == 'Python_Programs']
sys.path.extend(ROOT_FOLDER)

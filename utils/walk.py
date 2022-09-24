import os


def walk(root, ext='.pdf'):
    for dir_path, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(ext):
                yield os.path.join(dir_path, filename)
import os
import shutil

def copy_to_public(file_path_source, file_path_destination):
    if not os.path.exists(file_path_destination):
        os.mkdir(file_path_destination)
    source = os.path.abspath(file_path_source)
    dest = os.path.abspath(file_path_destination)
    file_list = os.listdir(source)
    for filename in file_list:
        file_path_s = os.path.join(source, filename)
        file_path_d = os.path.join(dest, filename)
        if os.path.isfile(file_path_s):
            print(f"Copying * {file_path_s} to {file_path_d}")
            shutil.copy(file_path_s, file_path_d)
        else: copy_to_public(file_path_s, file_path_d)
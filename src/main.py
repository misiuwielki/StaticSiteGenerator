import os
import shutil
from static_copy import copy_to_public
from page_generator import generate_page

def main():
    dir_path_public = "public"
    dir_path_static = "static"
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_to_public(dir_path_static, dir_path_public)
    generate_page("content/index.md", "template.html", "public/index.html")
    
main()
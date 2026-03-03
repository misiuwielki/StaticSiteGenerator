import os
import shutil
import sys
from static_copy import copy_to_public
from page_generator import generate_page, generate_page_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    dir_path_public = "public"
    dir_path_static = "static"
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_to_public(dir_path_static, dir_path_public)
    generate_page_recursive("content", "template.html", "docs", basepath)
    
main()
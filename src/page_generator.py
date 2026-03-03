from markdown_to_text import *
import re
import os
from pathlib import Path
from markdown_to_html import markdown_to_html

def extract_title(markdown):
    heading = re.search(r"^\# (.+)$", markdown, re.MULTILINE)
    if not heading:
        raise Exception("no h1 header found")
    return heading.group(1).strip()

def generate_page(source_path, template_path, dest_path):
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")
    with open(source_path, "r", encoding="utf-8") as f:
        source = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html = markdown_to_html(source)
    title = extract_title(source)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_page_recursive(source_dir_path, template_path, dest_dir_path):
    print(f"Generating pages from {source_dir_path} to {dest_dir_path} using {template_path}")
    source_list = os.listdir(source_dir_path)
    for filename in source_list:
        file_path = os.path.join(source_dir_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".md"):
            dest_path = Path(os.path.join(dest_dir_path, filename)).with_suffix(".html")
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()
            html = markdown_to_html(source)
            title = extract_title(source)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            print(f"Generating page from {file_path} to {dest_path}")
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(template)
        else: 
            dest_path = os.path.join(dest_dir_path, filename)
            generate_page_recursive (file_path, template_path, dest_path)
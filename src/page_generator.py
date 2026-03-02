from markdown_to_text import *
import re
import os
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
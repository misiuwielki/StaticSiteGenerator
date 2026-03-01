from textnode import TextNode, TextType
from enum import Enum
import re

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unordered list"
    OL = "ordered list"

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.PLAIN_TEXT:
                new_nodes.append(node)
                continue
            parts = node.text.split(delimiter)
            if len(parts) % 2 != 1 and delimiter in node.text:
                raise Exception("invalid Markdown syntax")
            for i in range(len(parts)):
                if parts[i] == "":
                     continue
                if i % 2 == 0:
                    new_node = TextNode(parts[i], TextType.PLAIN_TEXT)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(parts[i], text_type)
                    new_nodes.append(new_node)
        return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if node.text == "":
            continue
        if not images:
            new_nodes.append(node)
            continue
        alt_text = images[0][0]
        url = images[0][1]
        parts = node.text.split(f"![{alt_text}]({url})", 1)
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        if len(parts) > 1:
            new_nodes.extend(split_nodes_image([TextNode(parts[1], TextType.PLAIN_TEXT)]))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if node.text == "":
            continue
        if not links:
            new_nodes.append(node)
            continue
        alt_text = links[0][0]
        url = links[0][1]
        parts = node.text.split(f"[{alt_text}]({url})", 1)
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(alt_text, TextType.LINK_TEXT, url))
        if len(parts) > 1 and parts[1] != "":
            new_nodes.extend(split_nodes_link([TextNode(parts[1], TextType.PLAIN_TEXT)]))
    return new_nodes

def text_to_textnodes(text):
    bold = split_nodes_delimiter([TextNode(text, TextType.PLAIN_TEXT)], "**", TextType.BOLD_TEXT)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC_TEXT)
    code = split_nodes_delimiter(italic, "`", TextType.CODE_TEXT)
    images = split_nodes_image(code)
    links = split_nodes_link(images)
    return links

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda b: b.strip(), blocks))
    fixed_blocks = []
    for block in blocks:
        if block != "":
            fixed_blocks.append(block)
    return fixed_blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.H
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.C
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.Q
    if all(line.startswith("- ") for line in lines):
        return BlockType.UL
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.P
            i += 1
        return BlockType.OL
    #(
    #    (all(line[0].isdigit() for line in lines)
    #    and lines[0].startswith("1. ")
    #    and all(line.startswith(". ", 1) for line in lines[1:])
    #    and all((int(lines[i][0]) + 1 == int(lines[i+1][0])) for i in range(len(lines)-1)))
    #):
    return BlockType.P

def block_to_text(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.P:
        text = block
    elif block_type == BlockType.H:
        text = block.strip("#")
    elif block_type == BlockType.C:
        text = block.strip("```")
    else:
        text = block
    lines = text.split("\n")
    new_lines = ""
    if block_type == BlockType.Q:
        for line in lines:
            new_lines += line.strip(">") + "\n"
    elif block_type == BlockType.UL:
        for line in lines:
            new_lines += line.strip("- ") + "\n"
    elif block_type == BlockType.OL:
        i = 1
        for line in lines:
            new_lines += line.strip(f"{i}. ") + "\n"
            i += 1
    elif block_type == BlockType.P:
        for line in lines:
            new_lines += line + " "
    else:
        for line in lines:
            new_lines += line + "\n"
    if block_type != BlockType.C:
        new_lines = new_lines.strip()
    else: 
        print(repr(lines))
        return "\n".join(lines[1:-1]) + "\n"
    return new_lines

def heading_counter(block):
    return len(block) - len(block.lstrip("#"))
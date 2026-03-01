from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_to_text import *

HTML_tag_dict = {
    BlockType.P: "p",
    BlockType.H: "h",
    BlockType.C: "pre",
    BlockType.Q: "blockquote",
    BlockType.UL: "ul",
    BlockType.OL: "ol"
}

def markdown_to_html(markdown):
    mblocks = markdown_to_blocks(markdown)
    html_nodes = []
    for mblock in mblocks:
        block_type = block_to_block_type(mblock)
        block_text = block_to_text(mblock)
        leaf_nodes = []
        if block_type != BlockType.C:
            block_nodes = text_to_textnodes(block_text)
        elif block_type in {BlockType.OL, block_type.UL}:
            continue
        else:
            block_nodes = [TextNode(block_text, TextType.CODE_TEXT)]
        for node in block_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        if block_type not in {BlockType.H, BlockType.OL, BlockType.UL}:
            parent_node = ParentNode(HTML_tag_dict[block_type], leaf_nodes)
        elif block_type == BlockType.H:
            parent_node = ParentNode(f"{HTML_tag_dict[block_type]}{heading_counter(mblock)}", leaf_nodes)
        else:
            lines = block_text.split("\n")
            line_p_nodes = []
            for line in lines:
                line_nodes = text_to_textnodes(line)
                line_c_nodes = [text_node_to_html_node(node) for node in line_nodes]
                line_p_nodes.append(ParentNode("li", line_c_nodes))
            parent_node = ParentNode(HTML_tag_dict[block_type], line_p_nodes)
        html_nodes.append(parent_node)
    root_node = ParentNode("div", html_nodes)
    return root_node.to_html()
            
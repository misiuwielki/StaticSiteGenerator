import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_to_text import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks,
    block_to_block_type, BlockType, block_to_text
)


class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK_TEXT, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.boot.dev"})

    def test_image(self):
        node = TextNode("This is alt text on image node", TextType.IMAGE, "www.boot.dev/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "www.boot.dev/img.png", "alt": "This is alt text on image node"}
        )
    def test_inavlid_type(self):
        node = TextNode("This is a code node", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


class TestMarkdownToNodeSplitConversion(unittest.TestCase):
    def test_bold(self):
        node_1 = TextNode("This is a **bold** text node", TextType.PLAIN_TEXT)
        node_2 = TextNode("This **is** a **bold** text node", TextType.PLAIN_TEXT)
        node_3 = TextNode("**This is a bold text node**", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2, node_3]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" text node", TextType.PLAIN_TEXT),
                TextNode("This ", TextType.PLAIN_TEXT),
                TextNode("is", TextType.BOLD_TEXT),
                TextNode(" a ", TextType.PLAIN_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" text node", TextType.PLAIN_TEXT),
                TextNode("This is a bold text node", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )    
    def test_italic(self):
        node_1 = TextNode("This is an _italic_ text node", TextType.PLAIN_TEXT)
        node_2 = TextNode("This _is_ an _italic_ text node", TextType.PLAIN_TEXT)
        node_3 = TextNode("_This is an italic text node_", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2, node_3]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" text node", TextType.PLAIN_TEXT),
                TextNode("This ", TextType.PLAIN_TEXT),
                TextNode("is", TextType.ITALIC_TEXT),
                TextNode(" an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" text node", TextType.PLAIN_TEXT),
                TextNode("This is an italic text node", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    def test_code(self):
        node_1 = TextNode("This is a `code` node", TextType.PLAIN_TEXT)
        node_2 = TextNode("This `is` a `code` node", TextType.PLAIN_TEXT)
        node_3 = TextNode("`This is a code node`", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2, node_3]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE_TEXT),
                TextNode(" node", TextType.PLAIN_TEXT),
                TextNode("This ", TextType.PLAIN_TEXT),
                TextNode("is", TextType.CODE_TEXT),
                TextNode(" a ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE_TEXT),
                TextNode(" node", TextType.PLAIN_TEXT),
                TextNode("This is a code node", TextType.CODE_TEXT),
            ],
            new_nodes,
        )

    def test_invalid_syntax(self):
        node_1 = TextNode("This is a **bold text node", TextType.PLAIN_TEXT)
        nodes = [node_1]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)

    def test_bold_and_plain(self):
        node_1 = TextNode("This is a **bold** text node", TextType.PLAIN_TEXT)
        node_2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" text node", TextType.PLAIN_TEXT),
                TextNode("This is a text node", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )


class TestMarkdownLinkAndImageExtraction(unittest.TestCase):
    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_link_with_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertEqual([], matches)

    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_image_with_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertEqual([], matches)
        
    def test_no_links(self):
        text = "This is plain text"
        text2 = ""
        matches = [extract_markdown_links(text), extract_markdown_links(text2)]
        self.assertListEqual([[], []], matches)

    def test_no_images(self):
        text = "This is plain text"
        text2 = ""
        matches = [extract_markdown_images(text), extract_markdown_images(text2)]
        self.assertListEqual([[], []], matches)
    
    def test_link_halves(self):
        text = "This is text with a link [](https://www.boot.dev) and [to youtube]()"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://www.boot.dev"), ("to youtube", "")], matches)
    
    def test_image_halves(self):
        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![obi wan]()"
        matches = extract_markdown_images(text)
        self.assertEqual([("", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "")], matches)

    def text_mixed(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and image of ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = [extract_markdown_links(text), extract_markdown_images(text)]
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)



class TestMarkdownLinkAndImageSplit(unittest.TestCase):
    maxDiff = None
    def test_link(self):
        node_1 = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        node_2 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with further unnecessary text", TextType.PLAIN_TEXT)
        node_3 = TextNode("**This is a bold text node**", TextType.PLAIN_TEXT)
        node_4 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT)
        node_5 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        node_6 = TextNode("**This is a bold text node**", TextType.BOLD_TEXT)
        node_7 = TextNode("`This is a code node`", TextType.CODE_TEXT)
        node_8 = TextNode("[Link to boot dev](https://www.boot.dev) and a word", TextType.PLAIN_TEXT)
        node_9 = TextNode("[Link to boot dev](https://www.boot.dev)[and to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN_TEXT)
        node_10 = TextNode("This is text with a link [](https://www.boot.dev) and [to youtube]()", TextType.PLAIN_TEXT)
        node_11 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [it's copy](https://www.boot.dev)", TextType.PLAIN_TEXT)
        node_12 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"),
                TextNode(" with further unnecessary text", TextType.PLAIN_TEXT),
                TextNode("**This is a bold text node**", TextType.PLAIN_TEXT),
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT),
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"), 
                TextNode("**This is a bold text node**", TextType.BOLD_TEXT),
                TextNode("`This is a code node`", TextType.CODE_TEXT),
                TextNode("Link to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and a word", TextType.PLAIN_TEXT),
                TextNode("Link to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode("and to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"),
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("to youtube", TextType.LINK_TEXT, ""),
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("it's copy", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev")
            ],
            new_nodes)

    def test_images(self):
        node_1 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT)
        node_2 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with further unnecessary text", TextType.PLAIN_TEXT)
        node_3 = TextNode("**This is a bold text node**", TextType.PLAIN_TEXT)
        node_4 = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        node_5 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        node_6 = TextNode("**This is a bold text node**", TextType.BOLD_TEXT)
        node_7 = TextNode("`This is a code node`", TextType.CODE_TEXT)
        node_8 = TextNode("![Image](https://i.imgur.com/zjjcJKZ.png) and a word", TextType.PLAIN_TEXT)
        node_9 = TextNode("![Image](https://i.imgur.com/zjjcJKZ.png)![and second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN_TEXT)
        node_10 = TextNode("This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![obi wan]()", TextType.PLAIN_TEXT)
        node_11 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![same image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT)
        node_12 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT)
        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with further unnecessary text", TextType.PLAIN_TEXT),
                TextNode("**This is a bold text node**", TextType.PLAIN_TEXT),
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT),
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT),
                TextNode("**This is a bold text node**", TextType.BOLD_TEXT),
                TextNode("`This is a code node`", TextType.CODE_TEXT),
                TextNode("Image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a word", TextType.PLAIN_TEXT),
                TextNode("Image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("and second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("obi wan", TextType.IMAGE, ""),
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("same image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes)
        
class TestUltimateMarkdownToNodeConversion(unittest.TestCase):
    maxDiff = None
    def test_mixed(self):
        text_1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_2 = ""
        text_3 = "text"
        text_4 = "This is **text** with an **italic** word and a **code block**"
        text_5 = "**This is text** with an _italic word and a_`code block`"
        text_6 = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        text_7 = "[link](https://boot.dev)"
        texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7]
        nodes = [node for text in texts for node in text_to_textnodes(text)]
        self.assertListEqual(
            [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            TextNode("text", TextType.PLAIN_TEXT),
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.BOLD_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.BOLD_TEXT),
            TextNode("This is text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic word and a", TextType.ITALIC_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev")
            ],
            nodes)
        
    def test_markdown_to_nodes(self):
        text_1 = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        text_2= """

This is **bolded** paragraph


"""
        text_3 = """
           

          

This is **bolded** paragraph
"""
        texts = [text_1, text_2, text_3]
        blocks = [block for text in texts for block in markdown_to_blocks(text)]
        self.assertEqual(blocks,
                         ["This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "This is **bolded** paragraph",
                "This is **bolded** paragraph"
            ],)
        
    def test_block_type_check(self):
        block_1 = "# heading"
        block_2 = "###### heading"
        block_3 = "###not heading"
        block_4 = "#$#$#$# not heading"
        block_5 = """```
code
```"""
        block_6 = "```notcode```"
        block_7 = """> quote
>also quote"""
        block_8 = """>quote
no quote
>also quote"""
        block_9 = """- list
- list
- list"""
        block_10 = """- list
-not list"""
        block_11 = """1. list
2. list"""
        block_12 = """1. list
2.not a list"""
        block_13 = "10. not a list"
        block_14 = """1. text
2. text
3. text
4. text
5. text
6. text
7. text
8. text
9. text
10. text
11. text"""

        blocks = [
            block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8,
            block_9, block_10, block_11, block_12, block_13, block_14]
        block_types = list(map(block_to_block_type, blocks))
        self.assertListEqual(block_types, [
            BlockType.H,  #1
            BlockType.H,  #2
            BlockType.P,  #3
            BlockType.P,  #4
            BlockType.C,  #5
            BlockType.P,  #6
            BlockType.Q,  #7
            BlockType.P,  #8
            BlockType.UL, #9
            BlockType.P,  #10
            BlockType.OL, #11
            BlockType.P,  #12
            BlockType.P,  #13
            BlockType.OL, #14
        ])


    def test_ExtractBlockText(self):
        block_1 = "# heading"
        block_2 = "###### heading"
        block_3 = "###not heading"
        block_4 = "#$#$#$# not heading"
        block_5 = """```
code
```"""
        block_6 = "```notcode```"
        block_7 = """> quote
>also quote"""
        block_8 = """>quote
no quote
>also quote"""
        block_9 = """- list
- list
- list"""
        block_10 = """- list
-not list"""
        block_11 = """1. list
2. list"""
        block_12 = """1. list
2.not a list"""
        block_13 = "10. not a list"
        block_14 = """1. text
2. text
3. text
4. text
5. text
6. text
7. text
8. text
9. text
10. text
11. text"""

        blocks = [
            block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8,
            block_9, block_10, block_11, block_12, block_13, block_14]
        block_texts = list(map(block_to_text, blocks))
        self.assertListEqual(block_texts, [
            "heading", #1
            "heading", #2
            "###not heading", #3
            "#$#$#$# not heading", #4
            """code\n""", #5
            "```notcode```", #6
            """quote
also quote""", #7
            """>quote no quote >also quote""", #8
            """list
list
list""", #9
            """- list -not list""", #10
            """list
list""", #11
            """1. list 2.not a list""", #12
            "10. not a list", #13
            """text
text
text
text
text
text
text
text
text
text
text""" #14
        ])




if __name__ == "__main__":
    unittest.main()
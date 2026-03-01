import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_html import markdown_to_html

class TestSimpleConversion(unittest.TestCase):
    maxDiff = None
    def test_single(self):
        text_1 = "This is text"
        text_2 = "# A heading"
        text_3 = "This is **text** with an _italic_ word and a `code block`"
        text_4 = """- list
- list
- list"""
        text_5 = """1. list
2. list"""
        text_6 = """> quote
>also quote"""
        text_7 = """```
This is **text** with an _italic_ word and a `code block`
```"""
        text_8 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        text_9 = """This is a paragraph
that spans multiple lines."""
        texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7, text_8, text_9]
        html = [markdown_to_html(text) for text in texts]
        self.assertListEqual(html, [
            "<div><p>This is text</p></div>", #1
            "<div><h1>A heading</h1></div>", #2
            "<div><p>This is <b>text</b> with an <i>italic</i> word and a <code>code block</code></p></div>", #3
            "<div><ul><li>list</li><li>list</li><li>list</li></ul></div>", #4
            "<div><ol><li>list</li><li>list</li></ol></div>", #5
            "<div><blockquote>quote\nalso quote</blockquote></div>", #6
            "<div><pre><code>This is **text** with an _italic_ word and a `code block`\n</code></pre></div>", #7
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>", #8
            "<div><p>This is a paragraph that spans multiple lines.</p></div>", #9
        ])
        
    def test_mixed(self):
        text_1 = """# Heading

This is a paragraph with **bold** text.

- item one
- item two"""
        texts = [text_1]
        html = [markdown_to_html(text) for text in texts]
        self.assertListEqual(html, [
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>item one</li><li>item two</li></ul></div>"
        ])
import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is also a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a link", TextType.LINK_TEXT, "www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK_TEXT)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

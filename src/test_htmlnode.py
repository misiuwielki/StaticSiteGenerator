import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "a paragraph")
        node2 = HTMLNode("p", "a paragraph")
        self.assertEqual(node, node2)
    
    def test_neq_tag(self):
        node = HTMLNode("p", "a paragraph")
        node2 = HTMLNode("a", "a paragraph")
        self.assertNotEqual(node, node2)
    
    def test_neq_value(self):
        node = HTMLNode("p", "a paragraph")
        node2 = HTMLNode("p", "also a paragraph")
        self.assertNotEqual(node, node2)

    def test_neq_children(self):
        node = HTMLNode("p", "a paragraph", "one")
        node2 = HTMLNode("p", "a paragraph")
        self.assertNotEqual(node, node2)

    def test_eq_children_def(self):
        node = HTMLNode("p", "a paragraph", None)
        node2 = HTMLNode("p", "a paragraph")
        self.assertEqual(node, node2)

    def test_neq_props(self):
        node = HTMLNode("p", "a paragraph", None, "prop")
        node2 = HTMLNode("p", "a paragraph")
        self.assertNotEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "a paragraph")
        node2 = LeafNode("p", "a paragraph")
        self.assertEqual(node, node2)
    
    def test_neq_tag(self):
        node = LeafNode("p", "a paragraph")
        node2 = LeafNode("a", "a paragraph")
        self.assertNotEqual(node, node2)
    
    def test_neq_value(self):
        node = LeafNode("p", "a paragraph")
        node2 = LeafNode("p", "also a paragraph")
        self.assertNotEqual(node, node2)
    
    def test_eq_to_html_p(self):
        node = LeafNode("p", "a paragraph")
        self.assertEqual(node.to_html(), "<p>a paragraph</p>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()

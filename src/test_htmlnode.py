import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_1(self):
        node1 = HTMLNode("p", "some text content for this paragraph")
        node2 = HTMLNode("p", "some text content for this paragraph")
        self.assertEqual(repr(node1), repr(node2))

    def test_eq_2(self):
        node1 = HTMLNode("a", "bootdev", None, {"href": "http://www.boot.dev"})
        node2 = HTMLNode("a", "bootdev", None, {"href": "http://www.boot.dev"})
        self.assertEqual(repr(node1), repr(node2))
    
    def test_uneq_1(self):
        node1 = HTMLNode("img", None, None, {"src": "url/of/image.jpg", "alt": "this is a test"})
        node2 = HTMLNode("img", None, None, {"src": "url/of/image.jpg", "alt": "This is a test"})
        self.assertNotEqual(repr(node1), repr(node2))

    def test_uneq_2(self):
        node1 = HTMLNode("code", "def some_function(): pass", None, None)
        node2 = HTMLNode("p", "def some_function(): pass", None, None)
        self.assertNotEqual(repr(node1), repr(node2))

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">boot.dev</a>')

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print(\"Hello, world!\")")
        self.assertEqual(node.to_html(), "<code>print(\"Hello, world!\")</code>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "some text meant for a paragraph")
        self.assertEqual(node.to_html(), "some text meant for a paragraph")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None, None).to_html()

if __name__ == "__main__":
    unittest.main()
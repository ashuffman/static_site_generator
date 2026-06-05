import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
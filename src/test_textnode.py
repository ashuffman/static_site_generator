import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.CODE, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE, "http://www.boot.dev")
        self.assertEqual(node, node2)

    def text_ineq_link(self):
        node = TextNode("This is a text node", TextType.CODE, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE, "http://www.boot.org")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
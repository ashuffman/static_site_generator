import unittest
from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_text_type_error(self):
        node = TextNode("visit boot.dev", TextType.LINK, "https://boot.dev")
        new_nodes = split_nodes_delimiter([node], "[link]", TextType.LINK)
        self.assertEqual(new_nodes[0].__repr__(), node.__repr__())

    def test_unused_delimiter(self):
        node = TextNode("there is not bold text here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].__repr__(), node.__repr__())

    def test_bold(self):
        node1 = TextNode("this string contains **bold text**", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("this string contains ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD)
        ]
        self.assertEqual(split_nodes, expected_nodes)

    def test_italic(self):
        node1 = TextNode("this string contains _italic text_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node1], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("this string contains ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC)
        ]

    def test_odd_delimiters(self):
        node = TextNode("This string contains **no closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_code(self):
        node = TextNode("`code blocks` are also supported", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("code blocks", TextType.CODE),
            TextNode(" are also supported", TextType.TEXT)
        ]

    def test_delimiter_at_both_ends(self):
        node = TextNode("**this string is all bold baby!**", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("this string is all bold baby!", TextType.BOLD)
        ]
        self.assertEqual(split_nodes, expected_nodes)

    def test_multiple_old_nodes(self):
        node1 = TextNode("this string contains **bold type** elements", TextType.TEXT)
        node2 = TextNode("**this string is all bold baby!**", TextType.TEXT)
        node3 = TextNode("this is just a text string", TextType.TEXT)
        nodes = [node1, node2, node3]
        split_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("this string contains ", TextType.TEXT),
            TextNode("bold type", TextType.BOLD),
            TextNode(" elements", TextType.TEXT),
            TextNode("this string is all bold baby!", TextType.BOLD),
            TextNode("this is just a text string", TextType.TEXT)
        ]
        self.assertEqual(split_nodes, expected_nodes)
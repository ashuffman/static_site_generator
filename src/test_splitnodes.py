import unittest
from split_inline_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_text_nodes
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

class TestExtractNodes(unittest.TestCase):
    def test_single_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        test_list = extract_markdown_images(text)
        expected_list = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif")
        ]
        self.assertCountEqual(test_list, expected_list)

    def test_multi_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_list = extract_markdown_images(text)
        expected_list = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertCountEqual(test_list, expected_list)

    def test_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        test_list = extract_markdown_links(text)
        expected_list = [
            ("to boot dev", "https://www.boot.dev")
        ]
        self.assertEqual(test_list, expected_list)

    def test_multi_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test_list = extract_markdown_links(text)
        expected_list = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(test_list, expected_list)

    def test_no_img(self):
        text = "There are no links in this text"
        test_list = extract_markdown_images(text)
        expected_list = []
        self.assertEqual(test_list, expected_list)

    def test_no_link(self):
        text = "There are no links in this text"
        test_list = extract_markdown_links(text)
        expected_list = []
        self.assertEqual(test_list, expected_list)

    def test_empty_elements(self):
        text = "An empty image ![](https://boot.dev/img.png) and an empty link [empty]()"
        
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://boot.dev/img.png")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("empty", "")]
        )

    def test_empty_elements(self):
        text = "An empty image ![](https://boot.dev/img.png) and an empty link [empty]()"
        
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://boot.dev/img.png")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("empty", "")]
        )

    def test_broken_markdown(self):
        text = "This is [broken link (https://boot.dev) and ![broken image]https://boot.dev)"
        
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])    

class TestSplitNodesInline(unittest.TestCase):
    def test_link_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_img_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_img_with_both(self):
        node = TextNode("This is text with a link [to bootdev](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with a link [to bootdev](https://boot.dev) and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_link_with_both(self):
        node = TextNode("This is text with a link [to bootdev](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to bootdev", TextType.LINK, "https://boot.dev"),
            TextNode(" and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_multiple_link_nodes(self):
        node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            " and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        nodes = split_nodes_link([node1, node2])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(nodes, expected_nodes)        

    def test_multiple_image_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        node2 = TextNode(
            " and another ![second image](https://i.imgur.com/3elNhQu.png)", 
            TextType.TEXT    
        )
        nodes = split_nodes_image([node1, node2])
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_only(self):
        node = TextNode("this string contains only text", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        img_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("this string contains only text", TextType.TEXT)
        ]
        self.assertListEqual(link_nodes, expected_nodes)
        self.assertListEqual(img_nodes, expected_nodes)

class TestTextToNodes(unittest.TestCase):
    def test_all_text_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_empty_string(self):
        text = ""
        nodes = text_to_text_nodes(text)
        expected_nodes = []
        self.assertListEqual(nodes, expected_nodes)
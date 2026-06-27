from markdown_to_html import *
import unittest
import re

class TestMarkDownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- this is an unordered item
- so is this
- so is this
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>this is an unordered item</li><li>so is this</li><li>so is this</li></ul></div>"
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """
1. one
2. two
3. three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        self.assertEqual(html, expected)

    def test_block_quote(self):
        md = """
>Well done is better than well said.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>Well done is better than well said.</blockquote></div>"
        self.assertEqual(html, expected)

    def test_heading(self):
        md = "### Zen and the Art of Motorcycle Maintenance"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h3>Zen and the Art of Motorcycle Maintenance</h3></div>"
        self.assertEqual(html, expected)
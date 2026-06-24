import unittest
from split_blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_distinct_blocks(self):
        md = """
This is a paragraph with ***bolded** text.

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "This is a paragraph with ***bolded** text.",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertListEqual(blocks, expected_blocks)

    def test_extra_newlines(self):
            md = """
This is a paragraph with ***bolded** text.



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            expected_blocks = [
                "This is a paragraph with ***bolded** text.",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
            self.assertListEqual(blocks, expected_blocks)

class TestBlockTypes(unittest.TestCase):
    def test_heading(self):
        block = "## this is an h2 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_non_heading(self):
        block = "this is not a heading ##"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code(self):
        block = """
```
this is a code block
with multiple lines
```
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_not_code(self):
        block = "this contains back-ticks ``` but is not code"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_incorrect_code(self):
        block = "``this is an incorrectly formed code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_block_a(self):
        block = "> this is a\n> multiline quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_block_b(self):
        block = """
> this is a
> multiline quote
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_wrong_quote_block(self):
        block = """
> this is an incorrectly formed
quote block
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ul(self):
        block = """
- this is
- an unordered
- list
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_non_ul(self):
        block = """
- this list
1. is mixed type
- which doesn't actually work
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ol(self):
        block = """
1. one
2. two
3. three
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OLIST)
from textnode import *
from split_inline_nodes import *
from split_blocks import *
from htmlnode import *
import re

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node_orchstrator(block))
    return ParentNode("div", children)

def block_type_to_tag(block_type: BlockType) -> str:
    tag_dict = {
        BlockType.PARAGRAPH: "p",
        BlockType.CODE: "pre",
        BlockType.QUOTE: "blockquote",
        BlockType.ULIST: "ul",
        BlockType.OLIST: "ol",
    }
    return tag_dict[block_type]

def strip_markdown_code(block):
    return block[4, -3]

def code_to_html_node(block):
    stripped_block = strip_markdown_code(block)
    text_node = TextNode(stripped_block, TextType.TEXT)
    leaf_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [leaf_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def text_to_children(block: str) -> list:
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def strip_markdown_paragraph(block):
    lines = block.split("\n")
    return " ".join(lines)

def paragraph_to_html_node(block):
    stripped_block = strip_markdown_paragraph(block)
    children = text_to_children(stripped_block)
    return ParentNode("p", children)

def strip_markdown_heading(block):
    return block[block.find(" ") + 1:]

def header_tag_constructor(block: str) -> str:
    level = block.count("#", 0, block.find(" "))
    tag = f"h{level}"
    return tag

def heading_to_html_node(block):
    tag = header_tag_constructor(block)
    stripped_block = strip_markdown_heading(block)
    children = text_to_children(stripped_block)
    return ParentNode(tag, children)

def strip_markdown_quote(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_lines.append(line[1:].strip())
    return " ".join(stripped_lines)

def quote_to_html_node(block):
    stripped_block = strip_markdown_quote(block)
    children = text_to_children(stripped_block)
    return ParentNode("blockquote", children)

def strip_markdown_ul(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        list_items.append(line[2:])
    return list_items

def ul_to_html_node(block):
    items = strip_markdown_ul(block)
    li_nodes = []
    for item in items:
        li_nodes.append(ParentNode("li", text_to_children(item)))
    return ParentNode("ul", li_nodes)

def strip_markdown_ol(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        list_items.append(line[line.find(" ") + 1:])
    return list_items

def ol_to_html_node(block):
    items = strip_markdown_ol(block)
    li_nodes = []
    for item in items:
        li_nodes.append(ParentNode("li", text_to_children(item)))
    return ParentNode("ol", li_nodes)

def block_to_html_node_orchstrator(block):
    blocktype = block_to_block_type(block)
    match blocktype:
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ULIST:
            return ul_to_html_node(block)
        case BlockType.OLIST:
            return ol_to_html_node(block)
        case _:
            raise Exception("Error: unsupported BlockType")
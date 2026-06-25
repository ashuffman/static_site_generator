import re
from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    strings = markdown.split("\n\n")
    blocks = []
    for string in strings:
        string = string.strip()
        if string != "":
            blocks.append(string)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
# had this working, now it's broken again will have to figure it out and fix it
    # split the block into lines
    lines = block.strip().split("\n")

    # check for heading
    if re.match(r"#{1,6}", block):
        return BlockType.HEADING

    # check for code block
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # check for multiline quote
    if block.strip().startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
            
    # check for unordered list
    if block.strip().startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    # check for ordered list
    if block.strip().startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    # default to normal paragraph
    return BlockType.PARAGRAPH
        

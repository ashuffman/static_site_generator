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
    
    # set up control flow for remaining BlockTypes
    quote = True
    ul = True
    ol = True

    # check for multiline quote
    for line in lines:
        if not line.startswith(">"):
            quote = False
    if quote == True:
        return BlockType.QUOTE
            
    # check for unordered list
    for line in lines:
        if not line.startswith("- "):
            ul = False
    if ul == True:
        return BlockType.ULIST

    # check for ordered list
    for line in lines:
        if not re.match(r"[0-9]+\. ", line):
            ol = False
    if ol == True:
        return BlockType.OLIST

    # default to normal paragraph
    return BlockType.PARAGRAPH
        

from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        delimiter_count = node.text.count(delimiter)
        if node.text_type != TextType.TEXT or delimiter_count == 0:
            new_nodes.append(node)
        elif delimiter_count % 2 != 0:
            raise Exception("Error: Node text delimiters must appear in pairs")
        else:
            new_nodes.extend(text_to_nodes_factory(node, delimiter, text_type))
    return new_nodes

def text_to_nodes_factory(node: TextNode, delimiter: str, text_type:TextType) -> list[TextNode]:
    use_new_type = False
    
    new_nodes = []
    substrings = node.text.split(delimiter)

    for string in substrings:
        if string != "":
            new_nodes.append(TextNode(string, text_type if use_new_type else TextType.TEXT))
        use_new_type = not use_new_type

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        # if node.text contains no images, append to the list as is
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            alt_text = image[0]
            src_url = image[1]
            img_md = f"![{alt_text}]({src_url})"
            # if the text string doesn't start with the image markdown - extract the first substring into a TextNode and remove it from the string
            if not text.startswith(img_md):
                substr = text.split(img_md, 1)[0]
                new_nodes.append(
                    TextNode(
                        substr,
                        TextType.TEXT
                    )
                )
                text = text.removeprefix(substr)
            # add the new img TextNode to new_nodes, and remove it form the text string
            new_nodes.append(
                TextNode(
                    alt_text, 
                    TextType.IMAGE,
                    src_url
                )
            )
            text = text.removeprefix(img_md)
        if len(text) > 0:
            new_nodes.append(
                TextNode(
                    text, 
                    TextType.TEXT
                )
                )
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        # if node.text contains no links, append to the list as is
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            link_text = link[0]
            src_url = link[1]
            link_md = f"[{link_text}]({src_url})"
            # if the text string doesn't start with the link markdown - extract the first substring into a TextNode and remove it from the string
            if not text.startswith(link_md):
                substr = text.split(link_md, 1)[0]
                new_nodes.append(
                    TextNode(
                        substr,
                        TextType.TEXT
                    )
                )
                text = text.removeprefix(substr)
            # add the new link TextNode to new_nodes, and remove it form the text string
            new_nodes.append(
                TextNode(
                    link_text, 
                    TextType.LINK,
                    src_url
                )
            )
            text = text.removeprefix(link_md)
        if len(text) > 0:
            new_nodes.append(
                TextNode(
                    text, 
                    TextType.TEXT
                )
                )
    return new_nodes
    
    


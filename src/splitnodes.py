from textnode import TextType, TextNode

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


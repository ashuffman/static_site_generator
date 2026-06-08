class HTMLNode():
    def __init__(
            self, 
            tag: str = None, 
            value: str = None, 
            children: list[HTMLNode] = None, 
            props: dict[str: str] = None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ""
        if self.props:
            for k, v in self.props.items():
                output += f' {k}="{v}"'
        return output
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            value: str, 
            props: dict[str: str] = None
            ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.props is not None:
            props = self.props_to_html()
            return f'<{self.tag}{props}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(
            self, tag : str, 
            children : list, 
            props : dict[str:str] = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: ParentNode objects must include a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Error: ParentNode objects must contain at least one child node")
        html_output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_output += child.to_html()
        html_output += f"</{self.tag}>"
        return html_output
    
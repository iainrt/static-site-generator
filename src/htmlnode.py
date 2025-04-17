from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag = None, # string representing HTML tag name
                 value = None, # string representing the value of th eHTML tag
                 children = None, # list of HTMLnode objects representing chikdren of this node
                 props = None): # dictionary representing attributes of a tag
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
            raise NotImplementedError
        
    def props_to_html(self):
        output = ""
        if self.props is None:
             return ""
        for key, value in self.props.items():
            output += f' {key}="{value}"'
        return output

    def __repr__(self):
        props_str = ""
        if self.props:
            props_list = []
            for key, value in self.props.items():
                props_list.append(f"{key}={value}")
            props_str = " ".join(props_list)
        
        return f"tag: {self.tag} value: {self.value} children: {self.children} props: {props_str}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children = [])

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            props_html = self.props_to_html()
            return f'<{self.tag}{props_html}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, props=props, children = children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag required")
        if self.children is None:
            raise ValueError("children required")
        
        # Start with opening tag and include props if they exist
        if self.props:
            props_str = ""
            for prop, value in self.props.items():
                props_str += f' {prop}="{value}"'
            html_string = f"<{self.tag}{props_str}>"
        else:
            html_string = f"<{self.tag}>"

        # add HTMLL from all children
        for child in self.children:
            html_string += child.to_html()

        # close the tag
        html_string += f"</{self.tag}>"

        return html_string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
            
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid TextType: {text_node.text_type}")
        

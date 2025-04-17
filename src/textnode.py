from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # method to check all properties of two TextNode are equal
    def __eq__(self, comparator):
        return (self.text == comparator.text and 
                self.text_type == comparator.text_type and 
                self.url == comparator.url)
        
    # string representation of the TextNode object
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

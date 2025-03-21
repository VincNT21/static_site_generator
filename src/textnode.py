from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node2):
        return (
            self.text == text_node2.text 
            and self.text_type == text_node2.text_type 
            and self.url == text_node2.url
        )

    def __repr__(self):
        if self.url == None:
            return f'TextNode({self.text}, {self.text_type})'
        else:
            return f'TextNode({self.text}, {self.text_type}, {self.url})'
    

def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return HTMLNode(None, text_node.text)
        if text_node.text_type == TextType.BOLD:
            return HTMLNode('b', None, [HTMLNode(None, text_node.text)])
        if text_node.text_type == TextType.ITALIC:
            return HTMLNode('i', None, [HTMLNode(None, text_node.text)])
        if text_node.text_type == TextType.CODE:
            return HTMLNode('code', None, [HTMLNode(None, text_node.text)])
        if text_node.text_type == TextType.LINK:
            return HTMLNode('a', None, [HTMLNode(None, text_node.text)], {'href': text_node.url})
        if text_node.text_type == TextType.IMAGE:
            return HTMLNode('img', None, None, {'src': text_node.url, 'alt': text_node.text})
        else:
            raise ValueError(f'Wrong text type: {text_node.text_type}')
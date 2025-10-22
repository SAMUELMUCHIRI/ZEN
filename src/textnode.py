from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain_text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    ANCHOR = "anchor_text"
    ALT = "alt_text"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if self.text_type == node.text_type:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"


def text_node_to_html_node(text_node):
    if (type(text_node)) != (type(TextNode("hi", "alt_text"))):
        raise Exception("Not a valid type")
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.ANCHOR:
            return LeafNode(tag="a", value=text_node.text, props=text_node.url)
        case TextType.ALT:
            return LeafNode(
                tag="img",
                value=None,
                props={"src": text_node.url, "alt": text_node.text},
            )

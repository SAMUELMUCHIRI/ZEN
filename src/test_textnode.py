import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq(self):
        text = "This is a text node"
        texttyp = TextType
        node = TextNode(text, texttyp)
        result = f"TextNode({text},{texttyp},{None})"
        self.assertEqual(repr(node), result)

    def test_eq(self):
        text = "This is a text node"
        texttyp = TextType
        url = "https://maximus.co.ke"
        node = TextNode(text, texttyp, url)
        self.assertNotEqual(node.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()

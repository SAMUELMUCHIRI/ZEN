from textnode import *
from htmlnode import *
from delimiters import *
from functions import *
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        found = ""
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        node2 = TextNode("This is node2 with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        for i in result:
            if node.text_type == i.text_type:
                found = i.text_type

        self.assertEqual(found, node.text_type)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.ALT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.ALT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.ANCHOR, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.ANCHOR, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

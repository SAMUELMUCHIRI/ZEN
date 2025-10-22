import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node", children=None, props=None)
        result = f"htmlnode(p,This is a text node,None,None)"

        self.assertEqual(repr(node), result)

    def test_props(self):
        prop_anchor = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        child = HTMLNode("p", "This is a text node", children=None, props=None)

        parent = HTMLNode("a", "This is a Backend", children=[child], props=prop_anchor)
        self.assertEqual(parent.props, prop_anchor)
        self.assertEqual(parent.tag, "a")
        self.assertEqual(parent.children[0].tag, "p")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

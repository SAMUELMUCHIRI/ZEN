from multiprocessing import Value
from typing_extensions import NoDefault
import regex as re
from htmlnode import HTMLNode, ParentNode
from textnode import *
from block import *

node = TextNode(
    "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
    TextType.PLAIN,
)

node2 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.PLAIN,
)


def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)[)]", text)
    return matches


def extract_markdown_link(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)[)]", text)
    return matches


def extract_markdown_bold(text):
    matches = re.findall(r"\*\*(.*?)\*\*", text)
    return matches


def extract_markdown_code(text):
    matches = re.findall(r"\`(.*?)\`", text)
    return matches


def extract_markdown_italic(text):
    matches = re.findall(r"\_(.*?)\_", text)
    return matches


def split_nodes_bold(old_nodes):
    result = []
    for nodes_in in old_nodes:
        if nodes_in.text_type == TextType.PLAIN:
            bolds = extract_markdown_bold(nodes_in.text)
            len_links = len(bolds)
            count_bold = 0
            count = 0
            lim = ""
            text = ""
            add = True
            for i in range(0, len(nodes_in.text)):
                if nodes_in.text[i] == "*":
                    lim = "*"
                    if count_bold == 1:
                        add = False
                        if text != "":
                            result.append(TextNode(text, TextType.PLAIN))
                            text = ""
                        count_bold += 1
                    elif count_bold == 0:
                        count_bold += 1
                    elif count_bold == 2:
                        count_bold += 1
                    else:
                        add = True
                        count_bold = 0
                        result.append(TextNode(bolds[count], TextType.BOLD))
                        count += 1
                else:
                    lim = ""
                if add == True and lim == "":
                    text = f"{text}{nodes_in.text[i]}"

            if text != "":
                result.append(TextNode(text, TextType.PLAIN))
        else:
            result.append(nodes_in)
    return result


def split_nodes_code(old_nodes):
    result = []
    for nodes_in in old_nodes:
        if nodes_in.text_type == TextType.PLAIN:
            codes = extract_markdown_code(nodes_in.text)

            count_bold = 0
            count = 0
            lim = ""
            text = ""
            add = True
            for i in range(0, len(nodes_in.text)):
                if nodes_in.text[i] == "`":
                    lim = "`"
                    if count_bold == 0:
                        add = False
                        if text != "":
                            result.append(TextNode(text, TextType.PLAIN))
                            text = ""
                        count_bold += 1

                    else:
                        add = True
                        count_bold = 0
                        result.append(TextNode(codes[count], TextType.CODE))
                        count += 1
                else:
                    lim = ""
                if add == True and lim == "":
                    text = f"{text}{nodes_in.text[i]}"

            if text != "":
                result.append(TextNode(text, TextType.PLAIN))
        else:
            result.append(nodes_in)
    return result


def split_nodes_italics(old_nodes):
    result = []
    for nodes_in in old_nodes:
        if nodes_in.text_type == TextType.PLAIN:
            codes = extract_markdown_italic(nodes_in.text)

            count_bold = 0
            count = 0
            lim = ""
            text = ""
            add = True
            for i in range(0, len(nodes_in.text)):
                if nodes_in.text[i] == "_":
                    lim = "_"
                    if count_bold == 0:
                        add = False
                        if text != "":
                            result.append(TextNode(text, TextType.PLAIN))
                            text = ""
                        count_bold += 1

                    else:
                        add = True
                        count_bold = 0
                        result.append(TextNode(codes[count], TextType.ITALIC))
                        count += 1
                else:
                    lim = ""
                if add == True and lim == "":
                    text = f"{text}{nodes_in.text[i]}"

            if text != "":
                result.append(TextNode(text, TextType.PLAIN))
        else:
            result.append(nodes_in)
    return result


def split_nodes_link(old_nodes):
    result = []
    first_d = ""
    second_d = ")"
    for nodes_in in old_nodes:
        if nodes_in.text_type == TextType.PLAIN:
            links = extract_markdown_link(nodes_in.text)
            len_links = len(links)
            text = ""
            add = True
            count = 0
            for i in range(0, len(nodes_in.text)):
                if nodes_in.text[i] == "[":
                    first_d = "["
                    add = False
                    result.append(TextNode(text, TextType.PLAIN))

                    text = ""
                if add == True:
                    text = f"{text}{nodes_in.text[i]}"
                if (nodes_in.text[i] == ")") and (first_d == "["):
                    add = True
                    result.append(
                        TextNode(links[count][0], TextType.ANCHOR, links[count][1])
                    )
                    count += 1
            if text != "":
                result.append(TextNode(text, TextType.PLAIN))
        else:
            result.append(nodes_in)

    return result


def split_nodes_image(old_nodes):
    result = []
    first_d = ""
    second_d = ")"
    for nodes_in in old_nodes:
        links = extract_markdown_images(nodes_in.text)

        len_links = len(links)
        text = ""
        add = True
        count = 0
        for i in range(0, len(nodes_in.text)):
            if nodes_in.text[i] == "!":
                first_d = "!"
                add = False
                result.append(TextNode(text, TextType.PLAIN))
                text = ""
            if add == True:
                text = f"{text}{nodes_in.text[i]}"
            if (nodes_in.text[i] == ")") and (first_d == "!"):
                add = True
                result.append(TextNode(links[count][0], TextType.ALT, links[count][1]))
                count += 1
                first_d = ""
        if text != "":
            result.append(TextNode(text, TextType.PLAIN))
    return result


# new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]
test_cases_results = [
    [
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ANCHOR, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ANCHOR, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is text with a link", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ALT, "https://www.youtube.com/@bootdotdev"),
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ALT, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is ", TextType.PLAIN, None),
        TextNode("text", TextType.BOLD, None),
        TextNode(
            " with an _italic_ word and a `code block` and ", TextType.PLAIN, None
        ),
        TextNode("text", TextType.BOLD, None),
        TextNode(
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.PLAIN,
            None,
        ),
    ],
    [
        TextNode("This is **text** with an _italic_ word and a ", TextType.PLAIN, None),
        TextNode("code block", TextType.CODE, None),
        TextNode(
            " and **text** an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and ",
            TextType.PLAIN,
            None,
        ),
        TextNode("second code block", TextType.CODE, None),
        TextNode(
            "  a [link](https://boot.dev) **fgsdyafgas**   **text**",
            TextType.PLAIN,
            None,
        ),
    ],
    [
        TextNode("This is ", TextType.PLAIN, None),
        TextNode("text", TextType.BOLD, None),
        TextNode(" with an ", TextType.PLAIN, None),
        TextNode("italic", TextType.ITALIC, None),
        TextNode(" word and a ", TextType.PLAIN, None),
        TextNode("code block", TextType.CODE, None),
        TextNode(" and an ", TextType.PLAIN, None),
        TextNode("obi wan image", TextType.ALT, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAIN, None),
        TextNode("link", TextType.ANCHOR, "https://boot.dev"),
    ],
]


def text_to_textnodes(list_of_nodes):
    images_rm = split_nodes_image(list_of_nodes)
    links_rm = split_nodes_link(images_rm)
    bold_rm = split_nodes_bold(links_rm)
    italic_rm = split_nodes_italics(bold_rm)
    code_rm = split_nodes_code(italic_rm)
    return code_rm


md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """

markdown_result = """
    "This is **bolded** paragraph",


    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",


    "- This is a list\n- with items",
"""


def markdown_to_blocks(markdown):
    result = markdown.split("\n\n")
    result_strip = map(lambda x: x.strip(), result)
    rr = []
    for i in result_strip:
        y = i.split("\n")
        d = map(lambda x: x.strip(), y)
        rr.append("\n".join(d))
    result_remove_empty = filter(lambda x: x != "", rr)
    return list(result_remove_empty)


def text_to_children(string):
    pre_result = []
    pre_result.append(TextNode(string, TextType.PLAIN))

    children = text_to_textnodes(pre_result)
    result = []
    for i in children:
        result.append(text_node_to_html_node(i))
    return result


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = "<div>"
    for i in blocks:
        block_type = block_to_block_type(i)
        match block_type:
            case BlockType.p:
                parent_node = ParentNode(tag="p", children=None)
                if "\n" in i:
                    children_node = text_to_children(i)
                    sub_parent = ParentNode(tag="pre", children=children_node)
                    # print(sub_parent.to_html())
                    result = f"{result}<p>{sub_parent.to_html()}</p>"

                else:
                    children_node = text_to_children(i)
                    parent_node.children = children_node

                    result = f"{result}{parent_node.to_html()}"
                """    h = "heading"
                cd = "code"
                qt = "quote"
                ul = "unordered_list"
                ol = "ordered_list"
                """
            case BlockType.cd:
                parent_node = ParentNode(tag="code", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                # print(parent_node.to_html())
                result = f"{result}{parent_node.to_html()}"
            case BlockType.qt:
                parent_node = ParentNode(tag="q", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                # print(parent_node.to_html())
                result = f"{result}{parent_node.to_html()}"
            case BlockType.ul:
                parent_node = ParentNode(tag="ul", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                # print(parent_node.to_html())
                result = f"{result}{parent_node.to_html()}"

            case BlockType.ol:
                parent_node = ParentNode(tag="ol", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                # print(parent_node.to_html())
                result = f"{result}{parent_node.to_html()}"

            case _:
                parent_node = ParentNode(tag="p", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                # print(parent_node.to_html())
                result = f"{result}{parent_node.to_html()}"

                # list of children in htmlNodes

    return f"{result}</div>"


test_mark = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
[
    ["This is **bolded** paragraph", "text in a p", "tag here"],
    ["This is another paragraph with _italic_ text and `code` here"],
]
"""
[
    htmlnode(p,None,
        [
            htmlnode(None,This is ,None,None),
            htmlnode(b,bolded,None,None),
            htmlnode(None, paragraph,None,None),
            htmlnode(None,text in a p,None,None),
            htmlnode(None,tag here,None,None)
        ],None)
    htmlnode(p,None,
        [
            htmlnode(None,This is another paragraph with ,None,None),
            htmlnode(i,italic,None,None),
            htmlnode(None, text and ,None,None),
            htmlnode(code,code,None,None),
            htmlnode(None, here,None,None)
        ],None)
]
"""
# print(list(map(lambda x: x.split("\n"), markdown_to_blocks(test_mark))))

print(markdown_to_html_node(markdown_result))

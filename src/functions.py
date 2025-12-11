import os
from multiprocessing import Value
from threading import ExceptHookArgs

import regex as re
from typing_extensions import NoDefault

from block import *
from htmlnode import HTMLNode, ParentNode
from testdata import *
from textnode import *

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
    # print(f"Old nodes are {old_nodes}")
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
    # print(old_nodes)
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
            # print(if (len(links) > 0) )
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


sss = [
    TextNode("Want to get in touch?", TextType.PLAIN, None),
    TextNode("Contact me here", TextType.ANCHOR, "/contact"),
    TextNode(".", TextType.PLAIN, None),
    TextNode("This site was generated with a custom-built", TextType.PLAIN, None),
    TextNode(
        "static site generator",
        TextType.ANCHOR,
        "https://www.boot.dev/courses/build-static-site-generator-python",
    ),
    TextNode(" from the course on ", TextType.PLAIN, None),
    TextNode("Boot.dev", TextType.ANCHOR, "https://www.boot.dev"),
    TextNode(".", TextType.PLAIN, None),
]


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
                if len(text) > 0:
                    result.append(TextNode(text, TextType.PLAIN))
                text = ""
            if add == True:
                text = f"{text}{nodes_in.text[i]}"
            if (nodes_in.text[i] == ")") and (first_d == "!"):
                add = True
                if len(links) == 1:
                    result.append(
                        TextNode(links[count][0], TextType.ALT, links[count][1])
                    )

                count += 1
                first_d = ""
        if text != "":
            result.append(TextNode(text, TextType.PLAIN))

    return result


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


    "- This is a list\n-with items",
"""


def list_method(i, parent_tag, delimiter):
    parent_node = ParentNode(tag=f"{parent_tag}", children=None)

    list_items = i.split(f"{delimiter}")
    list_node_list = []
    for list_item in list_items:
        if len(list_item) > 0:
            if list_item.endswith("\n"):
                list_item = list_item[:-1]
            if parent_tag == "ol":
                list_item = list_item[2:].strip()
            list_node = ParentNode(tag="li", children=None)
            list_node.children = text_to_children(list_item)
            list_node_list.append(list_node)

    parent_node.children = list_node_list
    return parent_node


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
    if string.startswith("```") and string.endswith("```"):
        new_string = string[3:-3]
        pre_result.append(TextNode(new_string, TextType.CODE))
    else:
        pre_result.append(TextNode(string, TextType.PLAIN))

    children = text_to_textnodes(pre_result)
    result = []
    for i in children:
        result.append(text_node_to_html_node(i))

    return result


def markdown_to_html_node(markdown):
    main = []
    blocks = markdown_to_blocks(markdown)

    result = ParentNode(tag="div", children=None)

    for i in blocks:
        block_type = block_to_block_type(i)

        match block_type:
            case BlockType.p:
                parent_node = ParentNode(tag="p", children=None)
                children_node = text_to_children(i)

                parent_node.children = children_node
                main.append(parent_node)

            case BlockType.cd:
                parent_node = ParentNode(tag="pre", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node
                main.append(parent_node)

            case BlockType.qt:
                parent_node = ParentNode(tag="blockquote", children=None)
                finalstring = ""
                for j in i.split(">"):
                    if len(j) > 0:
                        formated = j.replace("\n", "<br>")
                        finalstring = f"{finalstring}{formated}"
                children_node = text_to_children(finalstring)
                parent_node.children = children_node
                print(parent_node)

                main.append(parent_node)

            case BlockType.ul:
                parent_node = list_method(i, "ul", "- ")
                main.append(parent_node)

            case BlockType.ol:
                parent_node = list_method(i, "ol", "\n")
                main.append(parent_node)

            case _:
                parent_node = ParentNode(tag="p", children=None)
                children_node = text_to_children(i)
                parent_node.children = children_node

                main.append(parent_node)

    result.children = main
    return result


def extract_title(markdown):
    matches = re.findall(r"(?:(?<=\n)|^)#(?!#)\s+.*", markdown)
    if len(matches) == 0:
        raise Exception("No title found")
    return matches[0].strip("# ")


def extract_h2(markdown):
    matches = re.findall(r"(?:(?<=\n)|^)##(?!#)\s+.*", markdown)
    if len(matches) == 0:
        return False
    return list(map(lambda x: x.strip("## "), matches))


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    h2 = extract_h2(markdown)
    if h2:
        for h2_item in h2:
            initial_h2 = f"## {h2_item}"
            new_h2 = f"<h2>{h2_item}</h2>"
            html = html.replace(initial_h2, new_h2)
    initial_title = f"# {title}"
    new_heading = f"<h1>{title}</h1>"
    html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace(initial_title, new_heading)
    )
    if os.path.exists(os.path.dirname(dest_path)):
        write_file(dest_path, html)
    else:
        os.makedirs(os.path.dirname(dest_path))
        write_file(dest_path, html)

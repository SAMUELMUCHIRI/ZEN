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

    print(f"To text nodes {code_rm}")

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
                list_item = list_item[1:]
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
    print(blocks)

    result = ParentNode(tag="div", children=None)

    for i in blocks:
        block_type = block_to_block_type(i)
        print(f"Block Type: {block_type}")
        match block_type:
            case BlockType.p:
                parent_node = ParentNode(tag="p", children=None)
                children_node = text_to_children(i)
                print(f"Children Node {children_node}")
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


"""

Read the markdown file at from_path and store the contents in a variable.
Read the template file at template_path and store the contents in a variable.
Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
Use the extract_title function to grab the title of the page.
Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
"""


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
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if os.path.exists(os.path.dirname(dest_path)):
        write_file(dest_path, html)
    else:
        os.makedirs(os.path.dirname(dest_path))
        write_file(dest_path, html)


"""
cwd = os.getcwd()
from_path = f"{cwd}/content/index.md"
template_path = f"{cwd}/template.html"
dest_path = f"{cwd}/public/index.html"
generate_page(from_path, template_path, dest_path)
"""
"""

test = [TextNode("![JRR Tolkien sitting](/images/tolkien.png)", TextType.PLAIN, None)]
print(split_nodes_image(test))
"""
print(markdown_to_html_node(test_markdown).to_html())
"""
print(
    text_to_textnodes(
        [
            TextNode(
                "![JRR Tolkien sitting](/images/tolkien.png)",
                TextType.PLAIN,
                None,
            )
        ]
    )
)
"""

"""
[TextNode(# Tolkien Fan Club,TextType.PLAIN,None)]
[TextNode(JRR Tolkien sitting,TextType.ALT,/images/tolkien.png)]
[TextNode(Here's the deal, ,TextType.PLAIN,None), TextNode(I like Tolkien,TextType.BOLD,None), TextNode(.,TextType.PLAIN,None)]
[TextNode( "I am in fact a Hobbit in all but size."<br><br> -- J.R.R. Tolkien,TextType.PLAIN,None)]
[TextNode(## Blog posts,TextType.PLAIN,None)]
[TextNode(Why Glorfindel is More Impressive than Legolas,TextType.ANCHOR,/blog/glorfindel)]
[TextNode(Why Tom Bombadil Was a Mistake,TextType.ANCHOR,/blog/tom)]
[TextNode(The Unparalleled Majesty of "The Lord of the Rings",TextType.ANCHOR,/blog/majesty)]
[TextNode(## Reasons I like Tolkien,TextType.PLAIN,None)]
[TextNode(You can spend years studying the legendarium and still not understand its depths,TextType.PLAIN,None)]
[TextNode(It can be enjoyed by children and adults alike,TextType.PLAIN,None)]
[TextNode(Disney ,TextType.PLAIN,None), TextNode(didn't ruin it,TextType.ITALIC,None), TextNode( (okay, but Amazon might have),TextType.PLAIN,None)]
[TextNode(It created an entirely new genre of fantasy,TextType.PLAIN,None)]
[TextNode(## My favorite characters (in order),TextType.PLAIN,None)]
[TextNode(. Gandalf,TextType.PLAIN,None)]
[TextNode(. Bilbo,TextType.PLAIN,None)]
[TextNode(. Sam,TextType.PLAIN,None)]
[TextNode(. Glorfindel,TextType.PLAIN,None)]
[TextNode(. Galadriel,TextType.PLAIN,None)]
[TextNode(. Elrond,TextType.PLAIN,None)]
[TextNode(. Thorin,TextType.PLAIN,None)]
[TextNode(. Sauron,TextType.PLAIN,None)]
[TextNode(. Aragorn,TextType.PLAIN,None)]
[TextNode(Here's what ,TextType.PLAIN,None), TextNode(elflang,TextType.CODE,None), TextNode( looks like (the perfect coding language):,TextType.PLAIN,None)]
[TextNode(
func main(){
fmt.Println("Aiya, Ambar,TextType.PLAIN,None), TextNode(
}
,TextType.PLAIN,None)]
[TextNode(Want to get in touch? ,TextType.PLAIN,None), TextNode(Contact me here,TextType.ANCHOR,/contact), TextNode(.,TextType.PLAIN,None)]
[TextNode(This site was generated with a custom-built ,TextType.PLAIN,None), TextNode(static site generator,TextType.ANCHOR,https://www.boot.dev/courses/build-static-site-generator-python), TextNode( from the course on ,TextType.PLAIN,None), TextNode(Boot.dev,TextType.ANCHOR,https://www.boot.dev), TextNode(.,TextType.PLAIN,None)]"""

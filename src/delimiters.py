from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final = []
    for i in old_nodes:
        result = []
        firstpart = ""
        delimiterpart = ""
        lastpart = ""
        for y in range(0, len(i.text)):
            if i.text[y] == delimiter:
                result.append(y)
            if len(result) == 2:
                firstpart = f"{firstpart}{i.text[: (result[0])]}"
                lastpart = f"{lastpart}{i.text[(result[1] + 1) :]}"
                delimiterpart = f"{delimiterpart}{i.text[(result[0] + 1) : result[1]]}"

                final.append(TextNode(text=firstpart, text_type=TextType.PLAIN))
                final.append(TextNode(text=delimiterpart, text_type=text_type))
                final.append(TextNode(text=lastpart, text_type=TextType.PLAIN))

                break
    return final

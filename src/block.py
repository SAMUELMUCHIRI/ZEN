from enum import Enum


class BlockType(Enum):
    p = "paragraph"
    h = "heading"
    cd = "code"
    qt = "quote"
    ul = "unordered_list"
    ol = "ordered_list"
    pre = "pre"


def is_member(value):
    try:
        int(value)
        return True
    except:
        return False


def block_to_block_type(block):
    if block[0] == "#":
        return BlockType.h
    elif block[0:3] == "```" and block[-3:] == "```":
        return BlockType.cd
    elif block[0] == ">":
        return BlockType.qt
    elif block[0] == "-":
        return BlockType.ul
    elif is_member(block[0]):
        return BlockType.ol
    else:
        return BlockType.p

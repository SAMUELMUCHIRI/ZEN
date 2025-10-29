import unittest
from block import *


class TestBlock(unittest.TestCase):
    def test_eq(self):
        ordered_list = "1 This is a list"
        un_list = "- this is unordered list"
        paragraph = "THis is a paragraph"
        code = "``` This is Code ```"
        quote = "> This is a quote"
        heading = "# THis is a heading"

        ol_result = block_to_block_type(ordered_list)
        ul_result = block_to_block_type(un_list)
        p_result = block_to_block_type(paragraph)
        c_result = block_to_block_type(code)
        q_result = block_to_block_type(quote)
        h_result = block_to_block_type(heading)

        self.assertEqual(ol_result, BlockType.ol)
        self.assertEqual(ul_result, BlockType.ul)
        self.assertEqual(p_result, BlockType.p)
        self.assertEqual(c_result, BlockType.cd)
        self.assertEqual(q_result, BlockType.qt)
        self.assertEqual(h_result, BlockType.h)

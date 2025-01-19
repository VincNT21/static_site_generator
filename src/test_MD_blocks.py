import unittest
from MD_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMDtoNodes(unittest.TestCase):
    def tests(self):
        test_text = """# This is a heading\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n 
                    * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(test_text),
            [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                ]
        )

        test_text = """# This is a heading\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n 
                    This is another paragraph\n\n
                    * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(test_text),
            [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                'This is another paragraph', 
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                ]
        )

        test_text = """# This is a heading\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is the same paragraph\n\n
                    * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(test_text),
            [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is the same paragraph', 
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                ]
        )

        test_text = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertListEqual(
            markdown_to_blocks(test_text),
            [
                'This is **bolded** paragraph', 
                'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line', 
                '* This is a list\n* with items'
                ]
        )

class TestBlockType(unittest.TestCase):
    def tests(self):
        self.assertEqual(block_to_block_type('# heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('> quoting\n>still quoting'), BlockType.QUOTE)
        self.assertEqual(block_to_block_type('* list\n* listlist'), BlockType.UNORD_LIST)
        self.assertEqual(block_to_block_type('- list\n- listlist'), BlockType.UNORD_LIST)
        self.assertEqual(block_to_block_type('1. un\n2. deux'), BlockType.ORD_LIST)
        self.assertEqual(block_to_block_type('```\ncode\n```'), BlockType.CODE)
        self.assertEqual(block_to_block_type('# heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('random text'), BlockType.PARAGRAPH)


if __name__=='__main__':
    unittest.main()
import unittest

from inline_MD import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_links,
    split_nodes_images,
    text_to_textnodes
    )
from textnode import TextNode, TextType



class TestSplitNodes_bold_italic_code(unittest.TestCase):
    def test_one_element(self):
        ex1_bold = [TextNode("This is text with a **bold** word", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(ex1_bold, '**', TextType.BOLD),
            [TextNode('This is text with a ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' word', TextType.TEXT)]
        )

        ex1_italic = [TextNode("This is text with a *italic* word", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(ex1_italic, '*', TextType.ITALIC),
            [TextNode('This is text with a ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word', TextType.TEXT)]
        )
    
    def test_multiple_elements(self):
        ex2 = [TextNode("This is text with a `code block` word", TextType.TEXT), TextNode("Here is `one code` and `another code` block", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(ex2, '`', TextType.CODE),
            [
                TextNode('This is text with a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' word', TextType.TEXT), 
                TextNode('Here is ', TextType.TEXT), TextNode('one code', TextType.CODE), TextNode(' and ', TextType.TEXT), TextNode('another code', TextType.CODE), TextNode(' block', TextType.TEXT)]
        )

        ex2_multiple_types = [TextNode("This is text with a **bold** and a *italic* word", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(split_nodes_delimiter(ex2_multiple_types, '**', TextType.BOLD), '*', TextType.ITALIC),
            [TextNode('This is text with a ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' and a ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word', TextType.TEXT)]
        )

    def test_errors(self):
        ex_empty = []     
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(ex_empty, '**', TextType.BOLD)
        self.assertEqual(str(context.exception), 'node list is empty')

        ex_err2 = [TextNode("This is text *with a *italic* word", TextType.TEXT)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(ex_err2, '*', TextType.ITALIC)
        self.assertEqual(str(context.exception), 'delimiter not found or invalid number of delimiter')

        ex_err3 = [TextNode("This is text with a **bold* word", TextType.TEXT)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(ex_err3, '**', TextType.BOLD)
        self.assertEqual(str(context.exception), 'delimiter not found or invalid number of delimiter')

    def test_other_type(self):
        ex_other_type = [TextNode("code block", TextType.CODE), TextNode("This is text with a *italic* word", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(ex_other_type, '*', TextType.ITALIC),
            [
                TextNode('code block', TextType.CODE),
                TextNode('This is text with a ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word', TextType.TEXT)
            ]
        )

    def test_others(self):
        node_empty = [TextNode('This is ** empty', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(node_empty, '*', TextType.TEXT), 
            [TextNode('This is ', TextType.TEXT), TextNode(' empty', TextType.TEXT)]
            )
        node_multiple_spaces = [TextNode('This is *    spaced out      * text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(node_multiple_spaces, '*', TextType.ITALIC),
            [TextNode('This is ', TextType.TEXT), TextNode('    spaced out      ', TextType.ITALIC), TextNode(' text', TextType.TEXT)]
        )
        node_consecutive = [TextNode('This **bold** **text** here', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(node_consecutive, '**', TextType.BOLD),
            [
    TextNode("This ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" ", TextType.TEXT), 
    TextNode("text", TextType.BOLD),
    TextNode(" here", TextType.TEXT)
]
        )
        node_delimiter_start = [TextNode('**bold** text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(node_delimiter_start, '**', TextType.BOLD),
            [TextNode('bold', TextType.BOLD), TextNode(' text', TextType.TEXT)]
        )
        node_delimiter_end = [TextNode('text *italic*', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(node_delimiter_end, '*', TextType.ITALIC),
            [TextNode('text ', TextType.TEXT), TextNode('italic', TextType.ITALIC)]
        )

class TestExtractMD(unittest.TestCase):
    def test_extr_images(self):
        self.assertListEqual(
            extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"),
            [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        )

    def test_extr_links(self):
        self.assertListEqual(
            extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extr_link_and_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = []
        result.extend(extract_markdown_links(text))
        result.extend(extract_markdown_images(text))
        self.assertListEqual(
            result,
            [("to boot dev", "https://www.boot.dev"), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        )

    def test_special_cases(self):
        self.assertListEqual(extract_markdown_images(''), [])
        self.assertListEqual(extract_markdown_links(''), [])

        malformed_md = 'This is a [broken link(https://example.com)'
        self.assertListEqual(extract_markdown_links(malformed_md), [])

        special_characters = 'Check out [this & that](https://example.com?param1=foo&param2=foo)'
        self.assertListEqual(extract_markdown_links(special_characters), [('this & that', 'https://example.com?param1=foo&param2=foo')])

        self.assertListEqual(
            extract_markdown_links('[link1](url1)[link2](url2)'),
            [('link1', 'url1'), ('link2', 'url2')]
        )

class TestSplitNodes_links_and_images(unittest.TestCase):
    def test_links(self):
        node = [TextNode('text and [link](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'url')
            ]
            )
        node = [TextNode('text and[link](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text and', TextType.TEXT),
                TextNode('link', TextType.LINK, 'url')
            ]
            )
        node = [TextNode('[link](url) and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
                TextNode(' and text', TextType.TEXT)
            ]
            )
        node = [TextNode('[link](url)and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
                TextNode('and text', TextType.TEXT)
            ]
            )
        node = [TextNode('[link](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
            ]
            )
        node = [TextNode('text and [link](url) and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'url'),
                TextNode(' and text', TextType.TEXT)
            ]
            )
        node = [TextNode('[link](url) and text then [link2](url2)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
                TextNode(' and text then ', TextType.TEXT),
                TextNode('link2', TextType.LINK, 'url2')
            ]
            )
        node = [TextNode('text only', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text only', TextType.TEXT)
            ]
            )
        node = [TextNode('text and [link](url)[link2](url2)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'url'),
                TextNode('link2', TextType.LINK, 'url2')
            ]
            )
        node = [TextNode(' [link](url) ', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
            ]
            )
        node = [TextNode('[link](url) [link2](url2) [link3](url3)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('link', TextType.LINK, 'url'),
                TextNode('link2', TextType.LINK, 'url2'),
                TextNode('link3', TextType.LINK, 'url3')
            ]
            )
        node = [TextNode('[]()', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('', TextType.LINK, ''),
            ]
            )
        node = [TextNode('text and [link](url)', TextType.TEXT), TextNode('text and[link2](url2)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_links(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'url'),
                TextNode('text and', TextType.TEXT),
                TextNode('link2', TextType.LINK, 'url2')
            ]
            )
    def test_images(self):
        node = [TextNode('text and ![alt_text](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('alt_text', TextType.IMAGE, 'url')
            ]
            )
        node = [TextNode('text and![alt_text](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('text and', TextType.TEXT),
                TextNode('alt_text', TextType.IMAGE, 'url')
            ]
            )
        node = [TextNode('![alt_text](url) and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode(' and text', TextType.TEXT)
            ]
            )
        node = [TextNode('![alt_text](url)and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode('and text', TextType.TEXT)
            ]
            )
        node = [TextNode('![alt_text](url)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
            ]
            )
        node = [TextNode('text and ![alt_text](url) and text', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode(' and text', TextType.TEXT)
            ]
            )
        node = [TextNode('![alt_text](url) and text then ![alt_text2](url2)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode(' and text then ', TextType.TEXT),
                TextNode('alt_text2', TextType.IMAGE, 'url2')
            ]
            )
        node = [TextNode('text only', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('text only', TextType.TEXT)
            ]
            )
        node = [TextNode('text and ![alt_text](url)![alt_text2](url2)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('text and ', TextType.TEXT),
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode('alt_text2', TextType.IMAGE, 'url2')
            ]
            )
        node = [TextNode(' ![alt_text](url) ', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
            ]
            )
        node = [TextNode('![alt_text](url) ![alt_text2](url2) ![alt_text3](url3)', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('alt_text', TextType.IMAGE, 'url'),
                TextNode('alt_text2', TextType.IMAGE, 'url2'),
                TextNode('alt_text3', TextType.IMAGE, 'url3')
            ]
            )
        node = [TextNode('![]()', TextType.TEXT)]
        self.assertListEqual(
            split_nodes_images(node),
            [
                TextNode('', TextType.IMAGE, ''),
            ]
            )

class TestTextToTextNodes(unittest.TestCase):
    def test_text(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        )
        self.assertListEqual(
            text_to_textnodes('just some text'),
            [TextNode('just some text', TextType.TEXT)]
        )
        self.assertListEqual(
            text_to_textnodes('**bold****bold2**'),
            [
                TextNode('bold', TextType.BOLD),
                TextNode('bold2', TextType.BOLD)
                ]
        )
        with self.assertRaises(ValueError) as context:
            text_to_textnodes('')
        self.assertEqual(str(context.exception), 'node list is empty')
        self.assertListEqual(
            text_to_textnodes(' '),
            [
                TextNode(' ', TextType.TEXT)
                ]
        )
        with self.assertRaises(ValueError) as context:
            text_to_textnodes('**bold* and *italic*')
        self.assertEqual(str(context.exception), 'delimiter not found or invalid number of delimiter')






if __name__ == "__main__":
    unittest.main()
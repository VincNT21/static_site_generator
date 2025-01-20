import unittest

from MD_to_HTML import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

class TestMD_to_HTML_node(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(
            markdown_to_html_node('#### This is heading with **bold text**').to_html(),
            '<div><h4>This is heading with <b>bold text</b></h4></div>'
            )
        
    def test_quote_blocks(self):
        self.assertEqual(
            markdown_to_html_node('>This is a quotation with **bold** text\n>on multiple lines').to_html(),
            '<div><blockquote>This is a quotation with <b>bold</b> text\non multiple lines</blockquote></div>'
        )

    def test_code_blocks(self):
        self.assertEqual(
            markdown_to_html_node('```\nThis is some code text with *italic* and `code` text in it\n```').to_html(),
            '<div><pre><code>This is some code text with <i>italic</i> and <code>code</code> text in it</code></pre></div>'
        )
        self.assertEqual(
            markdown_to_html_node('```\nThis is some code text\non multiple lines with *italic* and `code` text in it\n```').to_html(),
            '<div><pre><code>This is some code text\non multiple lines with <i>italic</i> and <code>code</code> text in it</code></pre></div>'
        )
        self.assertEqual(
            markdown_to_html_node('```\nThis is some code text\n    indented on multiple lines with *italic* and `code` text in it\n```').to_html(),
            '<div><pre><code>This is some code text\n    indented on multiple lines with <i>italic</i> and <code>code</code> text in it</code></pre></div>'
        )

    def test_unordered_lists(self):
        self.assertEqual(
            markdown_to_html_node('* This is line 1\n- This is line 2\n* This is line 3').to_html(),
            '<div><ul><li>This is line 1</li><li>This is line 2</li><li>This is line 3</li></ul></div>'
        )
        self.assertEqual(
            markdown_to_html_node('* Line 1 with *italic* text\n- Line 2 with `code` in it\n* Line 3 with [a link](https://example.com)').to_html(),
            '<div><ul><li>Line 1 with <i>italic</i> text</li><li>Line 2 with <code>code</code> in it</li><li>Line 3 with <a href="https://example.com">a link</a></li></ul></div>'
        )


    def test_ordered_lists(self):
        self.assertEqual(
            markdown_to_html_node('1. Ordered line 1\n2. Ordered line 2\n3. Ordered line 3').to_html(),
            '<div><ol><li>Ordered line 1</li><li>Ordered line 2</li><li>Ordered line 3</li></ol></div>'
        )
        self.assertEqual(
            markdown_to_html_node('1. This is **bold** line 1\n2. This is *italic* line 2\n3. This is ![alt text image](url/url/url.com) line 3').to_html(),
            '<div><ol><li>This is <b>bold</b> line 1</li><li>This is <i>italic</i> line 2</li><li>This is <img src="url/url/url.com" alt="alt text image"> line 3</li></ol></div>'
        )

    def test_paragraph_blocks(self):
        self.assertEqual(
            markdown_to_html_node('This is **bold** line 1\nThis is *italic* line 2\nThis is line 3').to_html(),
            '<div><p>This is <b>bold</b> line 1 This is <i>italic</i> line 2 This is line 3</p></div>'
        )

    def test_multiple_type_blocks(self):
        self.assertEqual(
            markdown_to_html_node('>This is a quotation with **bold** text\n>on multiple lines\n\n```\nThis is some code text with *italic* and `code` text in it\n```').to_html(),
            '<div><blockquote>This is a quotation with <b>bold</b> text\non multiple lines</blockquote><pre><code>This is some code text with <i>italic</i> and <code>code</code> text in it</code></pre></div>'
        )
        self.assertEqual(
            markdown_to_html_node('* This is line 1\n- This is line 2\n* This is line 3\n\n1. Ordered line 1\n2. Ordered line 2\n3. Ordered line 3').to_html(),
            '<div><ul><li>This is line 1</li><li>This is line 2</li><li>This is line 3</li></ul><ol><li>Ordered line 1</li><li>Ordered line 2</li><li>Ordered line 3</li></ol></div>'
        )

class TestExtract_Title(unittest.TestCase):
    def test_extract(self):
        md_doc = '> There is a code before everything\n> It is weird\n\n# This is the TITLE !\n\nThis is a paragraph text\nOn multiple lines#\n\n## Header 2\n\n* And also a list\n* With multiple items'
        self.assertEqual(extract_title(md_doc), 'This is the TITLE !')

if __name__ == '__main__':
    unittest.main()
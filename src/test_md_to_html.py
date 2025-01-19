import unittest

from MD_to_HTML import markdown_to_html_node
from htmlnode import HTMLNode

'''
class TestMD_to_HTML_node(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(
            markdown_to_html_node('#### This is heading with **bold text**'),
            HTMLNode('div', None, children: [HTMLNode('h4', None, children: [HTMLNode(None, 'This is heading with ', children: None, props: None), 'HTMLNode'('b', None, children: [HTMLNode(None, 'bold text', children: None, props: None)], props: None)], props: None)], props: None)
        )
'''


if __name__ == '__main__':
    unittest.main()
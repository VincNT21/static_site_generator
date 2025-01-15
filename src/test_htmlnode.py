import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode('h1', 'this is a test', None, {'href': 'https://www.rien.net', 'target': '_blank'})
        self.assertEqual(node.tag, 'h1')
        self.assertEqual(node.value, 'this is a test')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'href': 'https://www.rien.net', 'target': '_blank'})

    def test_repr(self):
        node = HTMLNode('h1', 'this is a test', None, {'href': 'https://www.rien.net'})
        self.assertEqual(node.__repr__(), "HTMLNode(h1, this is a test, children: None, props: {'href': 'https://www.rien.net'})")

    def test_props_to_html(self):
        node = HTMLNode('h1', 'this is a test', None, {'href': 'https://www.rien.net', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), ' href="https://www.rien.net" target="_blank"')




if __name__ == "__main__":
    unittest.main()
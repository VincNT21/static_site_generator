import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text nod", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url_None(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.rien.net")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.rien.net")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.rien.net")
        self.assertEqual(
            "TextNode(This is a text node, TextType.ITALIC, https://www.rien.net)",
            repr(node)
            )


class TestTexttoHTML(unittest.TestCase):
    def tests(self):
        text_node_TEXT = TextNode('simple text', TextType.TEXT)
        text_node_BOLD = TextNode('bold text', TextType.BOLD)
        text_node_ITALIC = TextNode('italic text', TextType.ITALIC)
        text_node_CODE = TextNode('code text', TextType.CODE)
        text_node_LINK = TextNode('link text', TextType.LINK, 'https://www.streetpress.com')
        text_node_IMAGE = TextNode('image alt text', TextType.IMAGE, 'https://www.sudeducation.org/wp-content/themes/sudeducation/logos/logo-sud-educ.svg')
        text_node_ERR = TextNode('text err', 'ERR')
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node_ERR)
        self.assertEqual(str(context.exception), 'Wrong text type: ERR')
        self.assertEqual(text_node_to_html_node(text_node_TEXT).__repr__(), 'LeafNode(None, simple text, props: None)')
        self.assertEqual(text_node_to_html_node(text_node_BOLD).__repr__(), 'LeafNode(b, bold text, props: None)')
        self.assertEqual(text_node_to_html_node(text_node_ITALIC).__repr__(), 'LeafNode(i, italic text, props: None)')
        self.assertEqual(text_node_to_html_node(text_node_CODE).__repr__(), 'LeafNode(code, code text, props: None)') 
        self.assertEqual(text_node_to_html_node(text_node_LINK).__repr__(), "LeafNode(a, link text, props: {'href': 'https://www.streetpress.com'})")
        self.assertEqual(
            text_node_to_html_node(text_node_IMAGE).__repr__(), 
            "LeafNode(img, , props: {'src': 'https://www.sudeducation.org/wp-content/themes/sudeducation/logos/logo-sud-educ.svg', 'alt': 'image alt text'})"
            )

if __name__ == "__main__":
    unittest.main()
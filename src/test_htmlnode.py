import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_values(self):
        leafnode = LeafNode('p', 'text in the leaf')
        self.assertEqual(leafnode.tag, 'p')
        self.assertEqual(leafnode.value, 'text in the leaf')
        self.assertEqual(leafnode.props, None)
        self.assertEqual(leafnode.children, None)

    def test_props(self):
        leafnode = LeafNode('a', 'link to click', {'href': 'https://www.streetpress.com'})
        self.assertEqual(leafnode.props, {'href': 'https://www.streetpress.com'})
        self.assertEqual(leafnode.props_to_html(), ' href="https://www.streetpress.com"')

    def test_to_html(self):
        leafnode = LeafNode('p', 'text in the leaf')
        self.assertEqual(leafnode.to_html(), '<p>text in the leaf</p>')


class TestParentNode(unittest.TestCase):
    def test_values(self):
        leafnode = LeafNode('p', 'text in the leaf')
        parentnode = ParentNode('h1', [leafnode], {'target': '_blank'})
        self.assertEqual(parentnode.tag, 'h1')
        self.assertEqual(parentnode.children, [leafnode])
        self.assertEqual(parentnode.props, {'target': '_blank'})

    def test_zero_children(self):
        leafnode = LeafNode('p', 'text in the leaf')
        parentnode_0 = ParentNode('h1', None)
        parentnode_0tag = ParentNode(None, [leafnode])
        parentnode_empty = ParentNode('h2', [])
        with self.assertRaises(ValueError) as context:
            parentnode_0.to_html()
        self.assertEqual(str(context.exception), 'Parent node must have children')
        with self.assertRaises(ValueError) as context:
            parentnode_0tag.to_html()
        self.assertEqual(str(context.exception), 'Parent node must have a tag')
        with self.assertRaises(ValueError) as context:
            parentnode_empty.to_html()
        self.assertEqual(str(context.exception), 'Parent node must have children')


    def test_to_html_onechild(self):
        leafnode1 = LeafNode('p', 'text in the leaf')
        parentnode_onechild = ParentNode('h1', [leafnode1])
        parentnode_onechild_withprops = ParentNode('h1', [leafnode1], {'target': '_blank'})
        self.assertEqual(parentnode_onechild.to_html(), '<h1><p>text in the leaf</p></h1>')
        self.assertEqual(parentnode_onechild_withprops.to_html(), '<h1 target="_blank"><p>text in the leaf</p></h1>')

    def test_to_html_children(self):
        leafnode1 = LeafNode('p', 'text in the leaf')
        leafnode2 = LeafNode('a', 'this is a link', {'href': 'https://www.streetpress.com'})
        leafnode3 = LeafNode('p', 'Another test text')
        parentnode = ParentNode('h2', [leafnode1, leafnode2])
        self.assertEqual(
            parentnode.to_html(), 
            '<h2><p>text in the leaf</p><a href="https://www.streetpress.com">this is a link</a></h2>'
            )
        grandparentnode = ParentNode('h1', [parentnode])
        self.assertEqual(
            grandparentnode.to_html(), 
            '<h1><h2><p>text in the leaf</p><a href="https://www.streetpress.com">this is a link</a></h2></h1>'
            )
        grandparentnode2 = ParentNode('h3', [leafnode3, grandparentnode], {'target': '_blank'})
        self.assertEqual(
            grandparentnode2.to_html(), 
            '<h3 target="_blank"><p>Another test text</p><h1><h2><p>text in the leaf</p><a href="https://www.streetpress.com">this is a link</a></h2></h1></h3>'
            )




if __name__ == "__main__":
    unittest.main()

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('method not implemented')
    
    def props_to_html(self):
        if self.props is None:
            return ''
        html_attributes = ''
        for item in self.props:
            html_attributes = html_attributes + ' ' + f'{item}="{self.props[item]}"'
        return html_attributes
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, props: {self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError('Leaf nodes must have a value')
        if self.tag == None:
            return f'{self.value}'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
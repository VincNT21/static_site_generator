
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('method not implemented')
    # A FAIRE EN CUMULANT LES DEUX CI DESSOUS CORRECTEMENT
    
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
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('Leaf node must have a value')
        if self.tag == None:
            return f'{self.value}'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, props: {self.props})'
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('Parent node must have a tag')
        if self.children is None or self.children == []:
            raise ValueError('Parent node must have children')
        children_nodes = ''
        for child in self.children:
            children_nodes += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_nodes}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode({self.tag}, children: {self.children}, props: {self.props})'

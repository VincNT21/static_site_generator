from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        raise ValueError('node list is empty')
    new_nodes = []
    for node in old_nodes:
        new_node = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text_in_list = node.text.split(delimiter)
            if len(text_in_list) % 2 == 0:
                raise ValueError('delimiter not found or invalid number of delimiter')
            for i, text in enumerate(text_in_list):
                if i % 2 == 0:
                    new_node.append(TextNode(text, TextType.TEXT))
                else:
                    new_node.append(TextNode(text, text_type))
            new_nodes.extend(new_node)
 
    return new_nodes
    
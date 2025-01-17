import re
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
                if text_in_list[i] == '':
                    continue
                if i % 2 == 0:
                    new_node.append(TextNode(text, TextType.TEXT))
                else:
                    new_node.append(TextNode(text, text_type))
            new_nodes.extend(new_node)
 
    return new_nodes
    
def extract_markdown_images(text):
    regex_for_images = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_for_images, text)

def extract_markdown_links(text):
    regex_for_links = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_for_links, text)

def split_nodes_images(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError('node list is empty')
    new_nodes = []
    for node in old_nodes:
        new_node = []
        original_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if extract_markdown_images(node.text) == []:
            new_nodes.append(node)
            continue
        for image in extract_markdown_images(node.text):
            alt_text = image[0]
            url = image[1]
            if original_text.split(f'![{alt_text}]({url})', 1)[0] == '':
                new_node.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                split_text = original_text.split(f'![{alt_text}]({url})', 1)[0]
                if split_text.strip() != '':    
                    new_node.append(TextNode(split_text, TextType.TEXT))
                new_node.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text = original_text.split(f'![{alt_text}]({url})', 1)[1]
        if original_text != '' and original_text.strip() != '':
            new_node.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_links(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError('node list is empty')
    new_nodes = []
    for node in old_nodes:
        new_node = []
        original_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
            continue
        for link in extract_markdown_links(node.text):
            link_text = link[0]
            url = link[1]
            if original_text.split(f'[{link_text}]({url})', 1)[0] == '':
                new_node.append(TextNode(link_text, TextType.LINK, url))
            else:
                split_text = original_text.split(f'[{link_text}]({url})', 1)[0]
                if split_text.strip() != '':
                    new_node.append(TextNode(split_text, TextType.TEXT))
                new_node.append(TextNode(link_text, TextType.LINK, url))
            original_text = original_text.split(f'[{link_text}]({url})', 1)[1]
        if original_text != '' and original_text.strip() != '':
            new_node.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(node, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '*', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_links(new_nodes)
    new_nodes = split_nodes_images(new_nodes)
    return new_nodes
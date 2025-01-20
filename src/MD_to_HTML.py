from MD_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_MD import text_to_textnodes
from textnode import TextType, TextNode, text_node_to_html_node

def extract_title(markdown):
    lines = markdown_to_blocks(markdown)
    for line in lines:
        if not line.startswith('# '):
            continue
        else:
            return line.removeprefix('# ')

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_nodes_children.append(convert_heading_block(block))
        if block_type == BlockType.QUOTE:
            block_nodes_children.append(convert_quote_block(block))
        if block_type == BlockType.CODE:
            block_nodes_children.append(convert_code_block(block))
        if block_type == BlockType.UNORD_LIST:
            block_nodes_children.append(convert_unordered_list_block(block))
        if block_type == BlockType.ORD_LIST:
            block_nodes_children.append(convert_ordered_list_block(block))
        if block_type == BlockType.PARAGRAPH:
            block_nodes_children.append(convert_paragraph_block(block))
    div_node = HTMLNode('div', None, block_nodes_children)
    return div_node

def text_to_children(text):
    children_text_nodes = text_to_textnodes(text)
    children_html_nodes = []
    for node in children_text_nodes:
        children_html_nodes.append(text_node_to_html_node(node))
    return children_html_nodes

def convert_heading_block(block):
    heading = block[0:block.find(' ')]
    heading_count = heading.count('#')
    block_text = block.removeprefix(f'{heading} ')
    children = text_to_children(block_text)
    return HTMLNode(f'h{heading_count}', None, children)

def convert_quote_block(block):
    lines = block.split('\n')
    text = '\n'.join(line.removeprefix('> ') for line in lines)
    children = text_to_children(text) 
    return HTMLNode('blockquote', None, children)

def convert_code_block(block):
    block = block.removeprefix('```\n')
    block = block.removesuffix('\n```')
    children = text_to_children(block)
    return HTMLNode('pre', None, [HTMLNode('code', None, children)])

def convert_unordered_list_block(block):
    block_split = block.split('\n')
    children = []
    for line in block_split:
        if line.startswith('* '):
            line = line.removeprefix('* ')
        elif line.startswith('- '):
            line = line.removeprefix('- ')
        grand_children = text_to_children(line)
        children.append(HTMLNode('li', None, grand_children))     
    return HTMLNode('ul', None, children)

def convert_ordered_list_block(block):
    block_split = block.split('\n')
    children = []
    i=1
    for line in block_split:
        line = line.removeprefix(f'{i}. ')
        i += 1
        grand_children = text_to_children(line)
        children.append(HTMLNode('li', None, grand_children))
    return HTMLNode('ol', None, children)

def convert_paragraph_block(block):
    lines = block.split('\n')
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    return HTMLNode('p', None, children)
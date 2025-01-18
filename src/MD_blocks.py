from enum import Enum

class BlockType(Enum):
    HEADING = 'heading'
    PARAGRAPH = 'paragraph'
    UNORD_LIST = 'unordered list'
    ORD_LIST = 'ordered list'
    QUOTE = 'quotes'
    CODE = 'code'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    result = []
    for block in blocks:
        block = block.strip()
        if block == '':
            continue
        result.append(block)
    return result

def block_to_block_type(md_block):
    lines = md_block.split('\n')
    if md_block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith('```') and lines[1].startswith('```'):
        return BlockType.CODE
    if md_block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if md_block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return BlockType.PARAGRAPH
        return BlockType.UNORD_LIST
    if md_block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORD_LIST
    if md_block.startswith('1. '):
        i=1
        for line in lines:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORD_LIST
    else:
        return BlockType.PARAGRAPH
    
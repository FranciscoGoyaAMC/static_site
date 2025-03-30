from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_to_textnodes, text_node_to_html_node
from blocktype import BlockType, block_to_block_type
import re

def markdown_to_blocks(markdown):
    """
    Divide um texto em Markdown em blocos separados por linhas em branco.
    """
    blocks = []
    for block in markdown.strip().split("\n\n"):
        lines = [line.strip() for line in block.split("\n")]        
        # Handling fenced code blocks (```)
        if block.startswith("```") and block.endswith("```"):
            blocks.append(lines[0])
            blocks.extend(lines[1:-1])
            blocks.append(lines[-1])        
        # Handling unordered lists (lines starting with "- ")
        elif all(line.startswith("- ") for line in lines):
            blocks.append("\n".join(line.strip() for line in lines))    
        # Handling ordered lists (lines starting with numbers followed by a period)
        elif all(re.match(r'^\d+\.', line) for line in lines):
            blocks.append("\n".join(line.strip() for line in lines))  
        # For everything else (paragraphs, etc.)
        else:
            blocks.append(" ".join(lines))
    return blocks


def text_to_children(text):
    """Converte um texto markdown inline em uma lista de HTMLNodes."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    """Converte um documento Markdown completo em um único nó HTMLNode."""
    blocks = markdown_to_blocks(markdown) 
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)       
        if block_type == BlockType.HEADING:
            level = block.count('#')  # Conta os '#' para definir o nível do heading
            text = block[level + 1:]  # Remove os '#' e o espaço seguinte
            children.append(ParentNode(f'h{level}', text_to_children(text)))       
        elif block_type == BlockType.CODE:
            code_text = block.strip('`')
            children.append(ParentNode("pre", [LeafNode("code", code_text)]))       
        elif block_type == BlockType.QUOTE:
            quote_text = block.replace('> ', '')
            children.append(ParentNode("blockquote", text_to_children(quote_text)))  
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split('\n')
            list_nodes = [ParentNode("li", text_to_children(item[2:])) for item in list_items]
            children.append(ParentNode("ul", list_nodes)) 
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.split('\n')
            list_nodes = []
            for item in list_items:
                if item.strip():
                    # Usando expressão regular para identificar a lista ordenada
                    match = re.match(r'^\d+\.\s+(.*)', item)
                    if match:
                        text = match.group(1)
                        list_nodes.append(ParentNode("li", text_to_children(text.strip())))
            children.append(ParentNode("ol", list_nodes))
        else:
            children.append(ParentNode("p", text_to_children(block)))
    return ParentNode("div", children)


def extract_title(markdown):
    """Extrai o título H1 do markdown."""
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):  # Verifica se a linha é um H1
            return line[2:].strip()  # Remove o "# " e os espaços extras
    
    raise ValueError("No H1 header found in the markdown file")

import re
from enum import Enum
from leafnode import LeafNode
from typing import List


class TextType(Enum):
    """Enumeração para representar os diferentes tipos de texto que podem ser usados em um TextNode."""
    NORMAL = "normal"       #Texto comum, sem formatação especial
    BOLD = "bold"           #Texto em negrito
    ITALIC = "italic"       #Texto em itálico
    CODE = "code"           #Texto formatado como código
    LINK = "link"           #Texto que representa um link (precisa de uma URL)
    IMAGE = "image"         #Representação de uma imagem (precisa de uma URL)
    HEADINGS = "heading"    #Representação de um título/cabeçalho


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        """Compara se dois objetos TextNode são iguais."""
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        """Retorna uma representação em string do objeto TextNode."""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """Converte um objeto TextNode em um objeto LeafNode correspondente com base no seu tipo (TextType)."""
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "",{"src": text_node.url,"alt": text_node.text})
    else:
        raise ValueError("Unsupported TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Divide um nó de texto normal usando um delimitador específico para definir um novo tipo."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue 

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}'")
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    """Extrai imagens em Markdown no formato ![alt text](URL)"""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """Extrai links em Markdown no formato [anchor text](URL)"""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    """Divide TextNodes em múltiplos nós baseando-se em imagens Markdown"""
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = sections[1] if len(sections) > 1 else ""

        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes):
    """Divide TextNodes em múltiplos nós baseando-se em links Markdown"""
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for link_text, url in links:
            sections = text.split(f"[{link_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = sections[1] if len(sections) > 1 else ""

        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    """Converte uma string de Markdown para uma lista de TextNodes"""
    nodes = [TextNode(text, TextType.NORMAL)]
    
    for delimiter, text_type in [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

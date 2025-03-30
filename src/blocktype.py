import re
from enum import Enum


class BlockType(Enum):
    """Enumeração dos tipos de blocos suportados pelo gerador de sites estáticos."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """
    Determina o tipo de bloco Markdown com base no seu formato.

    Regras:
    - Cabeçalhos: Começam com # (1-6) seguido de espaço.
    - Código: Começa e termina com ```.
    - Citação: Todas as linhas começam com >.
    - Lista não ordenada: Todas as linhas começam com "- ".
    - Lista ordenada: Todas as linhas começam com "1. ", "2. ", etc.
    - Caso contrário, é um parágrafo.

    Parâmetro:
    - block (str): Texto de um único bloco Markdown.

    Retorno:
    - BlockType: Enum representando o tipo do bloco.
    """
    lines = block.split("\n")
    # Verifica se é um cabeçalho (heading)
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    # Verifica se é um bloco de código (code)
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # Verifica se é uma citação (quote)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    # Verifica se é uma lista não ordenada (unordered list)
    if all(re.match(r"^- ", line) for line in lines):
        return BlockType.UNORDERED_LIST
    # Verifica se é uma lista ordenada (ordered list)
    if all(re.match(r"^\d+\. ", line) for line in lines):
        return BlockType.ORDERED_LIST
    # Caso contrário, é um parágrafo
    return BlockType.PARAGRAPH

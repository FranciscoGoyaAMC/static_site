import unittest
from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    """Testes para a função block_to_block_type."""

    def test_heading(self):
        """Testa cabeçalhos de diferentes níveis."""
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Small Heading"), BlockType.HEADING)

    def test_code_block(self):
        """Testa blocos de código cercados por três crases."""
        md = """```
def hello():
    print("Hello, world!")
```"""
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_quote_block(self):
        """Testa blocos de citação onde todas as linhas começam com '>'."""
        md = """> This is a quote
> that spans multiple lines."""
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_list(self):
        """Testa listas não ordenadas, onde todas as linhas começam com '- '."""
        md = """- Item 1
- Item 2
- Item 3"""
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        """Testa listas ordenadas, onde todas as linhas começam com números crescentes."""
        md = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        """Testa um parágrafo normal que não se encaixa em nenhum outro tipo."""
        md = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

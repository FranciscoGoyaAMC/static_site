import unittest
from markdown import markdown_to_blocks, extract_title


class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_paragraphs(self):
        md = """
        This is the first paragraph.

        This is the second paragraph.
        """
        expected = [
            "This is the first paragraph.",
            "This is the second paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_heading_and_paragraph(self):
        md = """
        # Heading

        This is a paragraph.
        """
        expected = [
            "# Heading",
            "This is a paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_code_block(self):
        md = """
        ```
        Code block here
        ```
        """
        expected = [
            "```",
            "Code block here",
            "```"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_list(self):
        md = """
        - Item 1
        - Item 2

        - Another list
        - With multiple items
        """
        expected = [
            "- Item 1\n- Item 2",
            "- Another list\n- With multiple items"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_mixed_content(self):
        md = """
        # Title

        Paragraph with **bold** text.

        > This is a quote.

        - List item
        - Another list item
        """
        expected = [
            "# Title",
            "Paragraph with **bold** text.",
            "> This is a quote.",
            "- List item\n- Another list item"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)
    
    def test_valid_h1(self):
        """Deve extrair corretamente um título H1."""
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_h1_with_extra_spaces(self):
        """Deve extrair um título H1 com espaços extras."""
        markdown = "#   Trimmed Title   "
        self.assertEqual(extract_title(markdown), "Trimmed Title")

    def test_multiple_headers(self):
        """Deve extrair o primeiro H1 em caso de múltiplos cabeçalhos."""
        markdown = "# First Title\n## Second Title\n# Another H1"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_missing_h1(self):
        """Deve levantar uma exceção se não houver H1."""
        markdown = "## No H1 Here\nJust some text"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in the markdown file")

    def test_empty_string(self):
        """Deve levantar uma exceção se a string estiver vazia."""
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_h1_with_symbols(self):
        """Deve extrair um título H1 com símbolos especiais."""
        markdown = "# Title with !@#$%^&*() symbols"
        self.assertEqual(extract_title(markdown), "Title with !@#$%^&*() symbols")



if __name__ == "__main__":
    unittest.main()

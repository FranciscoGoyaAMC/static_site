import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """Testa a renderização de uma tag de parágrafo <p>."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        """Testa a renderização de uma tag <a> com atributos."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_strong(self):
        """Testa a renderização de uma tag <strong>."""
        node = LeafNode("strong", "Bold text")
        self.assertEqual(node.to_html(), "<strong>Bold text</strong>")

    def test_leaf_to_html_without_tag(self):
        """Testa a renderização de um nó sem tag (texto bruto)."""
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_value_error(self):
        """Testa se a criação de um LeafNode sem valor levanta um erro."""
        with self.assertRaises(ValueError):
            LeafNode("p", None)


if __name__ == "__main__":
    unittest.main()

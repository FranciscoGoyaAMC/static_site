import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        """Verifica se os métodos props_to_html e __repr__ funcionam corretamente."""
        node = HTMLNode(tag="a", value="Click here")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        """Testa a conversão de atributos HTML quando há atributos fornecidos."""
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        """Testa a representação em string (__repr__) de um HTMLNode."""
        node = HTMLNode(tag="p", value="Hello, World!")
        self.assertEqual(repr(node), "HTMLNode(tag=p, value=Hello, World!, children=[], props={})")



if __name__ == "__main__":
    unittest.main()

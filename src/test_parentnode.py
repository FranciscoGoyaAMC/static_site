import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_one_child(self):
        """Testa a renderização de um ParentNode com um único filho"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        """Testa a renderização de um ParentNode com múltiplos filhos"""
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "More text"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i>More text</p>")

    def test_to_html_with_grandchildren(self):
        """Testa a renderização de um ParentNode com múltiplos filhos"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_parentnode_without_tag_raises_error(self):
        """Testa se a criação de um ParentNode sem tag levanta um erro"""
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "text")])

    def test_parentnode_without_children_raises_error(self):
        """Testa se a criação de um ParentNode sem filhos levanta um erro"""
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parentnode_with_props(self):
        """Testa a renderização de um ParentNode com atributos"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main"><span>child</span></div>')


if __name__ == "__main__":
    unittest.main()

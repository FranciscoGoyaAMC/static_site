import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from markdown import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        """Testa se dois objetos TextNode com as mesmas propriedades são iguais"""
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        """Testa se TextNode com textos diferentes são considerados diferentes"""
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1,node2)

    def test_eq_different_text_type(self):
        """Testa se TextNode com tipos de texto diferentes são considerados diferentes"""
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1,node2)
    
    def test_eq_url(self):
        """Testa se TextNode com URLs diferentes são considerados diferentes"""
        node1 = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://another.com")
        self.assertNotEqual(node1, node2)
    
    def test_default_url_none(self):
        """Testa se o URL padrão de TextNode é None"""
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
   
    def test_text(self):
        """Testa se um TextNode do tipo TEXT é corretamente convertido em um LeafNode sem tag."""  
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")   

    def test_bold_conversion(self):
        """Testa se um TextNode do tipo BOLD é corretamente convertido em um LeafNode com tag <b>."""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_conversion(self):
        """Testa se um TextNode do tipo ITALIC é corretamente convertido em um LeafNode com tag <i>."""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_conversion(self):
        """Testa se um TextNode do tipo CODE é corretamente convertido em um LeafNode com tag <code>."""
        node = TextNode("print('Hello, World!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, World!')")

    def test_link_conversion(self):
        """Testa se um TextNode do tipo LINK é corretamente convertido em um LeafNode com tag <a> e atributo href."""
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_conversion(self):
        """Testa se um TextNode do tipo IMAGE é corretamente convertido em um LeafNode com tag <img> e atributos src e alt."""
        node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Image description"})

    def test_invalid_text_type(self):
        """Testa se a função levanta um ValueError para um TextNode com um tipo inválido."""
        class FakeTextType:
            INVALID = "invalid"
        node = TextNode("Invalid", FakeTextType.INVALID)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_split_bold_delimiter(self):
        """Testa se a função divide corretamente um texto com delimitador de negrito."""
        node = TextNode("This is **bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_delimiter(self):
        """Testa se a função divide corretamente um texto com delimitador de itálico."""
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_code_delimiter(self):
        """Testa se a função divide corretamente um texto com delimitador de código."""
        node = TextNode("Here is `code` inside text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Here is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" inside text", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_matching_delimiter(self):
        """Testa se a função levanta erro quando não há um delimitador correspondente."""
        node = TextNode("This is **invalid text", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        """Testa se a função lida corretamente com múltiplos delimitadores no mesmo texto."""
        node = TextNode("Mixing _italic_ and **bold**", TextType.NORMAL)
        nodes_italic = split_nodes_delimiter([node], "_", TextType.ITALIC)
        nodes_both = split_nodes_delimiter(nodes_italic, "**", TextType.BOLD)
        expected = [
            TextNode("Mixing ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(nodes_both, expected)    

    def test_extract_markdown_images(self):
        """Testa se a função extrai corretamente o texto alternativo e URL de uma imagem no formato markdown"""
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("image", "https://i.imgur.com/zjjcJKZ.png")]
        )

    def test_extract_markdown_links(self):
        """Testa se a função extrai corretamente o texto do link e URL no formato markdown"""
        text = "Click [here](https://example.com) for more info."
        self.assertListEqual(
            extract_markdown_links(text),
            [("here", "https://example.com")]
        )

    def test_no_images(self):
        """Testa se a função retorna uma lista vazia quando não há imagens no formato markdown no texto."""
        text = "No images here!"
        self.assertListEqual(extract_markdown_images(text), [])


    def test_no_links(self):
        """Testa se a função retorna uma lista vazia quando o texto não contém links no formato markdown."""
        text = "No links here!"
        self.assertListEqual(extract_markdown_links(text), [])

    def test_split_images_single(self):
        """Testa se a função divide corretamente um TextNode contendo texto normal e uma imagem em nodes separados"""
        node = TextNode(
            "Here is an ![image](https://example.com/image.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here is an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_multiple(self):
        """Testa se a função divide corretamente um TextNode com múltiplas imagens em nodes individuais"""
        node = TextNode(
            "This is text with an ![image1](https://i.imgur.com/img1.png) and another ![image2](https://i.imgur.com/img2.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image1", TextType.IMAGE, "https://i.imgur.com/img1.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("image2", TextType.IMAGE, "https://i.imgur.com/img2.png"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        """Testa se a função retorna o TextNode original inalterado quando não há imagens no texto."""
        node = TextNode("This text has no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_links_single(self):
        """Testa se a função divide corretamente um TextNode contendo um link em nodes separados,
          convertendo o link para um TextNode do tipo LINK e mantendo o texto normal adjacente"""
        node = TextNode(
            "Here is a [link](https://example.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here is a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_multiple(self):
        """Testa se a função divide corretamente um TextNode com múltiplos links em nodes individuais,
          convertendo cada link para TextNode.LINK e preservando o texto normal entre eles."""
        node = TextNode(
            "This is a [site1](https://site1.com) and another [site2](https://site2.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("site1", TextType.LINK, "https://site1.com"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("site2", TextType.LINK, "https://site2.com"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_no_links(self):
        """Testa se a função retorna o próprio TextNode inalterado quando não há links no texto."""
        node = TextNode("This text has no links", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_images_and_links_mixed(self):
        """Testa se split_nodes_link e split_nodes_image processam corretamente um TextNode com links e imagens misturados,
          convertendo cada elemento para seu tipo específico enquanto mantém o texto normal intacto."""
        node = TextNode(
            "Click [here](https://example.com) to see an ![image](https://example.com/image.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)  # Aplicando ambas as funções
        expected = [
            TextNode("Click ", TextType.NORMAL),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to see an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_plain_text(self):
        """Testa se um texto simples sem marcação é processado corretamente."""
        text = "This is a simple text."
        expected = [TextNode("This is a simple text.", TextType.NORMAL)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        """Testa se um texto em negrito (**bold**) é processado corretamente."""
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        """Testa se um texto em itálico (_italic_) é processado corretamente."""
        text = "This is _italic_ text."
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        """Testa se um texto de código inline (`code`) é processado corretamente."""
        text = "This is `code`."
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        """Testa se uma imagem em Markdown (![alt](URL)) é processada corretamente."""
        text = "This is an ![image](https://example.com/image.jpg)"
        expected = [
            TextNode("This is an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        """Testa se um link em Markdown ([text](URL)) é processado corretamente."""
        text = "Click [here](https://example.com) to visit."
        expected = [
            TextNode("Click ", TextType.NORMAL),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to visit.", TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_markdown(self):
        """Testa se um texto contendo múltiplas marcações é processado corretamente."""
        text = "This is **bold**, _italic_, `code`, ![image](https://example.com/img.jpg), and [link](https://example.com)."
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(", and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_paragraph(self):
        """Testa um único parágrafo sem quebras de linha extras."""
        md = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_multiple_paragraphs(self):
        """Testa múltiplos parágrafos separados corretamente."""
        md = """This is the first paragraph.

        This is the second paragraph."""
        expected = [
            "This is the first paragraph.",
            "This is the second paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_blocks_with_inline_markdown(self):
        """Testa blocos contendo Markdown inline como negrito, itálico e código."""
        md = """This is **bolded** paragraph.

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line.

        - This is a list
        - with items"""
        expected = [
            "This is **bolded** paragraph.",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line.",
            "- This is a list\n- with items"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_extra_newlines(self):
        """Testa um Markdown com múltiplas quebras de linha extras entre blocos."""
        md = """First block.


        Second block.


        Third block."""
        expected = [
            "First block.",
            "Second block.",
            "Third block."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_and_trailing_whitespace(self):
        """Testa se espaços extras no início e no final são removidos."""
        md = """
    First block with spaces.

    Second block with more spaces.    
    """
        expected = [
            "First block with spaces.",
            "Second block with more spaces."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)


if __name__ == "__main__":
    unittest.main()

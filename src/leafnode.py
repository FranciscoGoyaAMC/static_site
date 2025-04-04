from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        if value is None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag=tag,value=value,children=None,props=props)

    def to_html(self):
        """
        Converte um nó (LeafNode) em HTML
        """
        if self.value is None:
            raise ValueError("LeafNode requires a value.")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
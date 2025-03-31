from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        if not children:
            raise ValueError("ParentNode requires at least one child.")
        if not tag:
            raise ValueError("ParentNode requires a tag.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """
        Converte um nó (ParentNode) em HTML
        """
        if self.children is None:
            raise ValueError("ParentNode requires at least one child.")
        if self.tag is None:
            raise ValueError("ParentNode requires a tag.")
        props_html = self.props_to_html() if self.props else ""
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
    
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        """Este método será implementado por classes filhas."""
        raise NotImplementedError
    
    def props_to_html(self):
        """Converte os atributos do nó em uma string de atributos HTML."""
        if not self.props:
            return ""
        else:
            return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
    def __repr__(self):
        """Retorna uma representação legível do objeto HTMLNode."""
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

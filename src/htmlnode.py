class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f"{key}={self.props[key]} "
        return result
    
    def __eq__(self, other):
        return (
            self.tag == other.tag and
             self.value == other.value and
              self.children == other.children and
              self.props == other.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
            super().__init__(tag, value, children=None, props=props)

    def to_html(self):
            if self.value == None:
                raise ValueError("LeafNode value is required")
            if not self.tag:
                return f"{self.value}"
            if self.props:
                return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
            f"LeafNode({self.tag}, {self.value}, {self.props})"
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
          super().__init__(tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
              raise ValueError("tag required for ParentNode")
        if self.children == None:
              raise ValueError("children required for ParentNode")
        output = f"<{self.tag}>"
        for child in self.children:
              child_o = child.to_html()
              output += child_o
        return output + f"</{self.tag}>"
    
    def __repr__(self):
            f"ParentNode({self.tag}, {self.children}, {self.props})"
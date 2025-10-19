class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This should be overwritten by a child class.")

    def props_to_html(self):
        if self.props == None:
            return ""
        
        result = ""
        for key in self.props:
            result += f' {key}="{self.props[key]}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: No Value.")
        if self.tag is None:
            return self.value
        if self.props:
            propsHTML = super().props_to_html()
            return f'<{self.tag}{propsHTML}>{self.value}</{self.tag}>'
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: Parent has no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: Parent has no children")
        else:
            result = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                result += child.to_html()
            return result + f"</{self.tag}>"
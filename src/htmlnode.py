from threading import ExceptHookArgs


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplemented)

    def props_to_html(self):
        result = ""
        for key, value in self.props.items():
            new_string = f'{key}="{value}" '
            result = f"{result}{new_string}"
        return result

    def __repr__(self):
        return f"htmlnode({self.tag},{self.value},{self.children},{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag != "img":
            if self.value == None:
                raise ValueError("All leaf nodes must have a value")
            if self.tag == None:
                return self.value
            if self.props == None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            return f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag} {super().props_to_html()}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __iter__(self):
        childrenVal = ""
        for i in self.children:
            childrenVal = f"{childrenVal}{i.to_html()}"

        return childrenVal

    def to_html(self):
        if self.tag is None:
            raise ValueError("Does not have a tag")
        if self.children is None:
            raise ValueError("Missing Children")

        return f"<{self.tag}>{self.__iter__()}</{self.tag}>"

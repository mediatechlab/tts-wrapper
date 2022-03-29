from abc import ABC, abstractmethod

Child = object


class AbstractSSMLNode(ABC):
    @abstractmethod
    def add(self, child: Child) -> "AbstractSSMLNode":
        pass


class SSMLNode(AbstractSSMLNode):
    def __init__(self, tag: str, attrs=None, children=None) -> None:
        self.tag = tag
        self.attrs = attrs or {}
        self.children = children or []

    def __str__(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attrs.items())
        rendered_children = "".join(str(c) for c in self.children)
        return f"<{self.tag}{(' ' if attrs else '')}{attrs}>{rendered_children}</{self.tag}>"

    def add(self, child: Child) -> "SSMLNode":
        self.children.append(child)
        return self

    @staticmethod
    def speak(attrs=None) -> "SSMLNode":
        return SSMLNode("speak", attrs)

    @staticmethod
    def voice(attrs=None) -> "SSMLNode":
        return SSMLNode("voice", attrs)

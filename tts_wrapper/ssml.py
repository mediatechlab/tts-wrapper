from abc import ABC, abstractmethod
from typing import Any, List, Mapping, Optional

Child = Any
Attr = Mapping[str, Any]


class AbstractSSMLNode(ABC):
    @abstractmethod
    def add(self, child: Child) -> "AbstractSSMLNode":
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...


class SSMLNode(AbstractSSMLNode):
    def __init__(
        self,
        tag: str,
        attrs: Optional[Attr] = None,
        children: Optional[List[Child]] = None,
    ) -> None:
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

    @classmethod
    def speak(cls, attrs: Optional[Attr] = None) -> "SSMLNode":
        return cls("speak", attrs)

    @classmethod
    def voice(cls, attrs: Optional[Attr] = None) -> "SSMLNode":
        return cls("voice", attrs)

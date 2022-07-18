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
        self._tag = tag
        self._attrs = attrs or {}
        self._children = children or []

    def __str__(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in self._attrs.items())
        rendered_children = "".join(str(c) for c in self._children)
        return f"<{self._tag}{(' ' if attrs else '')}{attrs}>{rendered_children}</{self._tag}>"

    def add(self, child: Child) -> "SSMLNode":
        self._children.append(child)
        return self

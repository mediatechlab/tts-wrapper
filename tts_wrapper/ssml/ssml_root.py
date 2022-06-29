from . import AbstractSSMLNode, Child, SSMLNode


class BaseSSMLRoot(AbstractSSMLNode):
    def __init__(self) -> None:
        self.inner = SSMLNode("speak")
        self.root = self.inner

    def __str__(self) -> str:
        return str(self.root)

    def add(self, child: Child) -> "AbstractSSMLNode":
        self.inner.add(child)
        return self

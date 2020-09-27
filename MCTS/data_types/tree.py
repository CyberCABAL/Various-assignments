from . import Node


class Tree:
    def __init__(self, root: Node = None):
        self.root = root if root is not None else Node()

    def set_root(self, new_root: Node):
        self.root = new_root

    def get_root(self) -> Node:
        return self.root

    def get_height(self):
        pass    # If needed later.

import random as r


class Node:
    def __init__(self, value=None, sub_nodes: list = None):
        self.value = value
        self.nodes = sub_nodes if sub_nodes is not None else []
        self.super_node = None

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def random_node(self):
        return r.choice(self.nodes)

    def get_node(self, index: int):
        return self.nodes[index] if 0 <= index < len(self.nodes) else None

    def set_node(self, index: int, node):
        if 0 <= index < len(self.nodes):
            self.nodes[index] = node

    def remove_node(self, index: int):
        if 0 <= index < len(self.nodes):
            del self.nodes[index]

    def get_nodes(self) -> list:
        return self.nodes

    def clear_nodes(self):
        self.nodes = []

    def set_nodes(self, sub_nodes: list):
        self.nodes = sub_nodes

    def is_empty(self):
        return len(self.nodes) == 0

    def num_nodes(self) -> int:
        return len(self.nodes)

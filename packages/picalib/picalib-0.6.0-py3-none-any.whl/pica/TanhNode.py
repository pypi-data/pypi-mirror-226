import math
from .Node import Node


class TanhNode(Node):
    def __init__(self, node):
        super(Node, self).__init__()
        self.value = node.result
        self.result = math.tanh((self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

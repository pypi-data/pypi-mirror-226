import math
from .Node import Node


class CscNode(Node):
    def __init__(self, node):
        super(CscNode, self).__init__()
        self.value = node.result
        self.result = 1 / (math.sin(math.radians(self.value)))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

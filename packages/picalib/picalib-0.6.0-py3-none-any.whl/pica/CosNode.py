import math
from .Node import Node


class CosNode(Node):
    def __init__(self, node):
        super(CosNode, self).__init__()
        self.value = node.result
        self.result = math.cos(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

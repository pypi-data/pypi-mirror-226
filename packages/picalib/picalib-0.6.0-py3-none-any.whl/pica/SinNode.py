import math
from .Node import Node


class SinNode(Node):
    def __init__(self, node):
        super(SinNode, self).__init__()
        self.value = node.result
        self.result = math.sin(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

import math
from .Node import Node


class TanNode(Node):
    def __init__(self, node):
        super(TanNode, self).__init__()
        self.value = node.result
        self.result = math.tan(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

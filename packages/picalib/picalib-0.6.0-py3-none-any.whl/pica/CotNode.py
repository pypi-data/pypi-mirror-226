import math
from .Node import Node


class CotNode(Node):
    def __init__(self, node):
        super(CotNode, self).__init__()
        self.value = node.result
        self.result = 1 / (math.tan(math.radians(self.value)))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

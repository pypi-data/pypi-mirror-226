import math
from .Node import Node


class CoshNode(Node):
    def __init__(self, node):
        super(CoshNode, self).__init__()
        self.value = node.result
        self.result = math.cosh((self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

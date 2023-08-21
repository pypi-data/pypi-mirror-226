import math
from .Node import Node


class SinhNode(Node):
    def __init__(self, node):
        super(SinhNode, self).__init__()
        self.value = node.result
        self.result = math.sinh((self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

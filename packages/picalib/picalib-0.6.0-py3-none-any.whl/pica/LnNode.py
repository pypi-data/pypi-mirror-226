import math
from .Node import Node


class LnNode(Node):
    def __init__(self, node):
        super(LnNode, self).__init__()
        self.value = node.result
        self.result = math.log(self.value)
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

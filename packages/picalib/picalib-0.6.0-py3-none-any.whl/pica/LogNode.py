import math
from .Node import Node


class LogNode(Node):
    def __init__(self, node):
        super(LogNode, self).__init__()
        self.value = node.result
        self.result = math.log(self.value, 10)
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)

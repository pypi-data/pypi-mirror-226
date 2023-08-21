import math
from .Node import Node

class ArcCosNode(Node):
    def __init__(self, node):
        super(ArcCosNode,self).__init__()
        self.value = node.result
        self.result = math.acos(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  

import math
from .Node import Node

class ArcTanNode(Node):
    def __init__(self, node):
        super(ArcTanNode,self).__init__()
        self.value = node.result
        self.result = math.atan(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  

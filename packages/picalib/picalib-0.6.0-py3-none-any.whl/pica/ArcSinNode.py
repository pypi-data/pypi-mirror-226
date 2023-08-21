import math
from .Node import Node

class ArcSinNode(Node):
    def __init__(self, node):
        super(ArcSinNode,self).__init__()
        self.value = node.result
        self.result = math.asin(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  

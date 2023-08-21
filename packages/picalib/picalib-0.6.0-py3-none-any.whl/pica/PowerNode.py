from .Node import Node


class PowerNode(Node):
    def __init__(self, node1, node2):
        super(PowerNode, self).__init__()
        self.value = node1.result
        self.exp = node2.result
        self.result = self.value**self.exp
        self.gradient = 0
        self.children = [node1, node2]
        self.parents = []
        node1.parents.append(self)
        node2.parents.append(self)

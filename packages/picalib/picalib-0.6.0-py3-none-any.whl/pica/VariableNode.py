from .Node import Node


class VariableNode(Node):
    def __init__(self, value):
        super(VariableNode, self).__init__()
        self.result = value
        self.gradient = 0
        self.children = []
        self.parents = []

from .Node import Node


class ValueNode(Node):
    def __init__(self, value):
        super(ValueNode, self).__init__()
        self.result = value
        self.gradient = 0
        self.children = []
        self.parents = []

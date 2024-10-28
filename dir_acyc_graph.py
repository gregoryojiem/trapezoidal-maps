class DAG:

class Node:
    def __init__(self):
        pass

class Internal(Node):
    def __init__(self):
        super().__init__()

class Leaf(Node):
    def __init__(self, trap):
        super().__init__()
        self.trap = trap

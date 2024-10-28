class DAG:
    def __init__(self):
        self.head = None


class Internal:
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class Leaf:
    def __init__(self, trap):
        super().__init__()
        self.trap = trap

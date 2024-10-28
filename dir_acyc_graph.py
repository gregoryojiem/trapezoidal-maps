class DAG:
    def __init__(self):
        self.head = None

    def resolve_case1(self): return None
    def resolve_case2(self): return None
    def resolve_case3(self): return None

    def create_output_matrix(self):
        return None


class Internal:
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class Leaf:
    def __init__(self, trap):
        super().__init__()
        self.trap = trap

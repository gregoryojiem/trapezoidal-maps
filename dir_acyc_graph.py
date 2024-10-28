class DAG:
    def __init__(self):
        self.head = None

    def add_new_segment(self, segment):
        pass

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

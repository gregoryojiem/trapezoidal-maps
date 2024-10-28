class DAG:
    def __init__(self):
        self.head = None

    def add_new_segment(self, segment):
        pass

    def create_output_matrix(self):
        return None


class Node:
    def __init__(self, data):
        self.data = data


class Internal:
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def is_child_left(self, node):
        if self.left == node:
            return True
        elif self.right == node:
            return False
        else:
            raise Exception("Not the parent of the child")


class Leaf:
    def __init__(self, trap):
        super().__init__()
        self.trap = trap

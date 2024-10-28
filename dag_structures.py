class Node:
    def __init__(self, data):
        self.data = data


class Internal:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_child_left(self, node):
        if self.left == node:
            return True
        elif self.right == node:
            return False
        else:
            raise Exception("Not the parent of the child")


class PointNode(Internal):
    def __init__(self, left, right, point):
        super().__init__(left, right)
        self.point = point


class SegNode(Internal):
    def __init__(self, left, right, seg):
        super().__init__(left, right)
        self.seg = seg


class Leaf:
    def __init__(self, trap):
        super().__init__()
        self.trap = trap
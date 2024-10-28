from dag_case1 import handle_case1
from dag_case2 import handle_case2
from dag_case3 import handle_case3


class DAG:
    def __init__(self, bounding_trapezoid):
        self.head = Node(Leaf(bounding_trapezoid))

    def add_new_segment(self, seg):
        affected_trapezoids = list(self.find_trapezoids(self.head, seg))

        if len(affected_trapezoids) == 1:
            handle_case2(seg, affected_trapezoids[0])
            return

        left_point_region = self.find_point_region(self.head, seg.p1)
        right_point_region = self.find_point_region(self.head, seg.p2)
        affected_trapezoids.remove(left_point_region)
        affected_trapezoids.remove(right_point_region)
        handle_case1(seg.p1, seg, left_point_region)
        handle_case1(seg.p2, seg, right_point_region)

        for trapezoid in affected_trapezoids:
            handle_case3(seg, trapezoid)

    def find_point_region(self, node, point):
        curr_node = node.data

        if isinstance(curr_node, Leaf):
            return node

        if isinstance(curr_node, PointNode):
            if not point.is_right_of(curr_node.point):
                return self.find_trapezoids(curr_node.left, point)
            else:
                return self.find_trapezoids(curr_node.right, point)

        if isinstance(curr_node, SegNode):
            if point.is_above(curr_node.seg):
                return self.find_trapezoids(curr_node.left, point)
            else:
                return self.find_trapezoids(curr_node.right, point)

    def find_trapezoids(self, node, seg):
        curr_node = node.data

        if isinstance(curr_node, Leaf):
            return {node}

        if isinstance(curr_node, PointNode):
            if not seg.p2.is_right_of(curr_node.point):  # segment is fully left of the point
                return {self.find_trapezoids(curr_node.left, seg)}
            elif seg.p1.is_right_of(curr_node.point):  # segment is fully right of the point
                return {self.find_trapezoids(curr_node.right, seg)}
            else:  # the point is in between the segment endpoints
                return {self.find_trapezoids(curr_node.right, seg)} \
                    .union({self.find_trapezoids(curr_node.left, seg)})

        if isinstance(curr_node, SegNode):
            if seg.is_above(curr_node.seg):
                return {self.find_trapezoids(curr_node.left, seg)}
            else:
                return {self.find_trapezoids(curr_node.right, seg)}

    def create_output_matrix(self):
        return None


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

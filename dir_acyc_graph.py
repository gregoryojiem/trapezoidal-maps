from dag_structures import Node, PointNode, SegNode, Leaf
from dag_case1 import handle_case1
from dag_case2 import handle_case2
from dag_case3 import handle_case3


class DAG:
    def __init__(self, bounding_trapezoid):
        self.head = Node(Leaf(bounding_trapezoid))

    def add_new_segment(self, seg):
        print("Adding new segment: " + str(seg))
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
                return self.find_point_region(curr_node.left, point)
            else:
                return self.find_point_region(curr_node.right, point)

        if isinstance(curr_node, SegNode):
            if point.is_above(curr_node.seg):
                return self.find_point_region(curr_node.left, point)
            else:
                return self.find_point_region(curr_node.right, point)

    def find_trapezoids(self, node, seg):
        curr_node = node.data

        if isinstance(curr_node, Leaf):
            return {node}

        if isinstance(curr_node, PointNode):
            if not seg.p2.is_right_of(curr_node.point):  # segment is fully left of the point
                return self.find_trapezoids(curr_node.left, seg)
            elif seg.p1.is_right_of(curr_node.point):  # segment is fully right of the point
                return self.find_trapezoids(curr_node.right, seg)
            else:  # the point is in between the segment endpoints
                return self.find_trapezoids(curr_node.right, seg) \
                    .union(self.find_trapezoids(curr_node.left, seg))

        if isinstance(curr_node, SegNode):
            seg_lowest_point = seg.get_lower_point()
            seg_higher_point = seg.get_higher_point()

            if not seg_higher_point.is_above(curr_node.seg.get_lower_point()):
                return self.find_trapezoids(curr_node.right, seg)
            elif seg_lowest_point.is_above(curr_node.seg.get_higher_point()):
                return self.find_trapezoids(curr_node.left, seg)
            else:
                return self.find_trapezoids(curr_node.right, seg) \
                    .union(self.find_trapezoids(curr_node.left, seg))

    def create_output_matrix(self):
        return None
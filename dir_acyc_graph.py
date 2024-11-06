from trapezoidal_map import Point
from dag_structures import Node, PointNode, SegNode, Leaf
from dag_case1 import handle_case1_left, handle_case1_right
from dag_case2 import handle_case2
from dag_case3 import handle_case3
import visualizations


class DAG:
    def __init__(self, bounding_trapezoid):
        self.head = Node(Leaf(bounding_trapezoid))

    def add_new_segment(self, seg, bbox):
        print("Adding new segment: " + str(seg))
        affected_trapezoids = list(self.find_trapezoids(self.head, seg))

        visualizations.regions_seen = []
        if len(affected_trapezoids) == 1:
            visualizations.plot_dag(self, bbox)
            handle_case2(seg, affected_trapezoids[0])
            return

        visualizations.plot_dag(self, bbox)

        left_point_region = self.find_point_region(self.head, seg.p1)
        right_point_region = self.find_point_region(self.head, seg.p2)
        affected_trapezoids.remove(left_point_region)
        affected_trapezoids.remove(right_point_region)
        degenerate_check_left = self.find_point(self.head, seg.p1)
        resultant_traps = handle_case1_left(seg.p1, seg, left_point_region, degenerate_check_left)
        visualizations.plot_dag(self, bbox)

        for trapezoid in affected_trapezoids:
            resultant_traps = handle_case3(seg, trapezoid, resultant_traps)
            visualizations.plot_dag(self, bbox)

        degenerate_check_right = self.find_point(self.head, seg.p2)
        handle_case1_right(seg.p2, seg, right_point_region, resultant_traps, degenerate_check_right)
        visualizations.plot_dag(self, bbox)

    def find_point(self, node, point):
        curr_node = node.data

        if isinstance(curr_node, Leaf):
            return None

        if isinstance(curr_node, PointNode) and curr_node.point.x == point.x and curr_node.point.y == point.y:
            return node

        left_point = self.find_point(curr_node.left, point)
        if left_point is not None:
            return left_point

        return self.find_point(curr_node.right, point)

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
                return self.find_trapezoids(curr_node.right, seg).union(self.find_trapezoids(curr_node.left, seg))

        if isinstance(curr_node, SegNode):
            left_x_bound = curr_node.seg.p1.x
            right_x_bound = curr_node.seg.p2.x
            point_to_compare = seg.p1 if seg.p1.within(left_x_bound, right_x_bound) else seg.p2

            if seg.p2 == curr_node.seg.p2 and seg.p1.is_above(curr_node.seg.p1):
                return self.find_trapezoids(curr_node.right, seg).union(self.find_trapezoids(curr_node.left, seg))
            if point_to_compare.is_above(curr_node.seg):
                return self.find_trapezoids(curr_node.left, seg)
            else:
                return self.find_trapezoids(curr_node.right, seg)

    def create_output_matrix(self):
        matrix = [[]]
        row1 = [None]

        left_points, right_points, segments, trapezoids = [], [], [], []
        self.traverse_all_nodes(self.head, left_points, right_points, segments, trapezoids)
        names = []
        for left_point in set(left_points):
            row1.append(left_point.point.name)
            names.append(left_point.point.name)
        for right_point in set(right_points):
            row1.append(right_point.point.name)
            names.append(right_point.point.name)
        for segment in set(segments):
            row1.append(segment.seg.name)
            names.append(segment.seg.name)
        trapezoids = ["T8", "T7", "T6", "T9", "T3", "T10", "T4"]  # todo remove this
        for trapezoid in set(trapezoids):
            row1.append(trapezoid)  # todo remove
            names.append(trapezoid)
        #     row1.append(trapezoid.trap.name)
        #     names.append(trapezoid.trap.name)
        row1.append("sum")
        matrix[0] = row1

        blank_row = [0] * len(row1)
        for i in range(1, len(row1)):
            matrix.append(blank_row[:])

        for i in range(1, len(matrix) - 1):
            matrix[i][0] = names[i - 1]

        matrix[-1][0] = "sum"
        matrix[-1][-1] = None

        # Calculate column sums
        for j in range(1, len(matrix) - 1):
            col_sum = 0
            for i in range(1, len(matrix) - 1):
                col_sum += matrix[i][j]
            matrix[-1][j] = col_sum

        # Calculate row sums and print
        for i in range(len(matrix)):
            if i not in (0, len(matrix) - 1):
                matrix[i][-1] = sum(matrix[i][1:])
            print(matrix[i])
        return matrix

    def traverse_all_nodes(self, node, left_points, right_points, segments, trapezoids):
        curr_node = node.data
        if isinstance(curr_node, PointNode):
            if "P" in curr_node.point.name:
                left_points.append(curr_node)
            else:
                right_points.append(curr_node)
            self.traverse_all_nodes(curr_node.left, left_points, right_points, segments, trapezoids)
            self.traverse_all_nodes(curr_node.right, left_points, right_points, segments, trapezoids)
            return
        if isinstance(curr_node, SegNode):
            segments.append(curr_node)
            self.traverse_all_nodes(curr_node.left, left_points, right_points, segments, trapezoids)
            self.traverse_all_nodes(curr_node.right, left_points, right_points, segments, trapezoids)
            return
        if isinstance(curr_node, Leaf):
            trapezoids.append(curr_node)
            return

import visualizations
import random
from data_structures.dag_structures import Node, PointNode, SegNode, Leaf
from dag_case1 import handle_case1_left, handle_case1_right
from dag_case2 import handle_case2
from dag_case3 import handle_case3

class DAG:
    def __init__(self, bounding_trapezoid, segments):
        self.head = Node(Leaf(bounding_trapezoid))
        self.randomized_incremental_algorithm(segments)

    def randomized_incremental_algorithm(self, segments):
        """
        Loops through all line segments in a randomized order and calls the DAG to update itself
        :param trap_map: TrapezoidalMap containing all important test_data
        :returns: Directed Acyclic Graph
        """
        # TODO remove seeding
        random.Random(4).shuffle(segments)
        for _ in range(0, len(segments)):
            segment = segments.pop(0)
            self.add_new_segment(segment)

    def add_new_segment(self, seg):
        print("Adding new segment: " + str(seg))
        affected_trapezoids = list(self.find_trapezoids(self.head, seg))

        visualizations.regions_seen = []
        if len(affected_trapezoids) == 1:
            visualizations.plot_dag(self, self.bbox)
            handle_case2(seg, affected_trapezoids[0])
            return

        visualizations.plot_dag(self, self.bbox)

        left_point_region = self.find_point_region(self.head, seg.p1)
        right_point_region = self.find_point_region(self.head, seg.p2)
        affected_trapezoids.remove(left_point_region)
        affected_trapezoids.remove(right_point_region)
        degenerate_check_left = self.find_point(self.head, seg.p1)
        resultant_traps = handle_case1_left(seg.p1, seg, left_point_region, degenerate_check_left)
        visualizations.plot_dag(self, self.bbox)

        affected_trapezoids.sort(key=lambda x: x.data.trap.left_vert.x)
        for trapezoid in affected_trapezoids:
            resultant_traps = handle_case3(seg, trapezoid, resultant_traps)
            visualizations.plot_dag(self, self.bbox)

        degenerate_check_right = self.find_point(self.head, seg.p2)
        handle_case1_right(seg.p2, seg, right_point_region, resultant_traps, degenerate_check_right)
        visualizations.plot_dag(self, self.bbox)

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

    def find_point_region(self, node, point, print_path=False):
        curr_node = node.data

        if print_path:
            print(curr_node)

        if isinstance(curr_node, Leaf):
            return node

        if isinstance(curr_node, PointNode):
            if not point.is_right_of(curr_node.point):
                return self.find_point_region(curr_node.left, point, print_path)
            else:
                return self.find_point_region(curr_node.right, point, print_path)

        if isinstance(curr_node, SegNode):
            if point.is_above(curr_node.seg):
                return self.find_point_region(curr_node.left, point, print_path)
            else:
                return self.find_point_region(curr_node.right, point, print_path)

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
                return self.find_trapezoids(curr_node.left, seg).union(self.find_trapezoids(curr_node.right, seg))

        if isinstance(curr_node, SegNode):
            seg_above = seg.is_above(curr_node.seg)

            if seg.p2 == curr_node.seg.p2 and seg_above:
                return self.find_trapezoids(curr_node.left, seg).union(self.find_trapezoids(curr_node.right, seg))
            if seg_above:
                return self.find_trapezoids(curr_node.left, seg)
            else:
                return self.find_trapezoids(curr_node.right, seg)

    def create_output_matrix(self):
        node_names = []
        connections_map = {}
        self.traverse_all_nodes(self.head, connections_map, node_names)
        node_names = list(set(node_names))
        node_names = sorted(node_names, key=lambda x: (x[0], int(x[1:])))

        matrix = [[]]
        row1 = [None]
        row1.extend(node_names)
        row1.append("sum")
        matrix[0] = row1

        blank_row = [0] * len(row1)
        for i in range(1, len(row1)):
            matrix.append(blank_row[:])
        for i in range(1, len(matrix) - 1):
            matrix[i][0] = row1[i]
        matrix[-1][0] = "sum"
        matrix[-1][-1] = None

        # Fill in table
        for i in range(1, len(matrix[0]) - 1):
            name = matrix[0][i]
            if 'T' in name:
                break
            connections = connections_map.get(name)
            for connection in connections:
                j = matrix[0].index(connection)
                matrix[j][i] = 1

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

    def traverse_all_nodes(self, node, connections_map, names):
        curr_node = node.data
        if isinstance(curr_node, PointNode):
            point_name = curr_node.point.name
            names.append(point_name)
            l_name = self.traverse_all_nodes(curr_node.left, connections_map, names)
            r_name = self.traverse_all_nodes(curr_node.right, connections_map, names)
            if point_name in connections_map:
                connections_map.get(point_name).append(l_name)
                connections_map.get(point_name).append(r_name)
            else:
                connections_map[point_name] = [l_name, r_name]
            return point_name
        if isinstance(curr_node, SegNode):
            seg_name = curr_node.seg.name
            names.append(seg_name)
            l_name = self.traverse_all_nodes(curr_node.left, connections_map, names)
            r_name = self.traverse_all_nodes(curr_node.right, connections_map, names)
            if seg_name in connections_map:
                connections_map.get(seg_name).append(l_name)
                connections_map.get(seg_name).append(r_name)
            else:
                connections_map[seg_name] = [l_name, r_name]
            return seg_name
        if isinstance(curr_node, Leaf):
            trap_name = curr_node.trap.name
            names.append(trap_name)
            return trap_name

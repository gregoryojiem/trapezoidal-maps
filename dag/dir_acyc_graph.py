import visualizations
# import random

from data_structures.dag_structures import Node, PointNode, SegmentNode, LeafNode
from dag.case1 import handle_case_1_left, handle_case1_right
from dag.case2 import handle_case_2
from dag.case3 import handle_case_3


class DAG:
    """
    A class that represents a directed acyclic graph composed of various nodes.
    Has various utility functions for tree building/traversal
    """

    def __init__(self, segments, bounding_trapezoid):
        self.head = Node(LeafNode(bounding_trapezoid))
        self.bbox = bounding_trapezoid
        self.randomized_incremental_algorithm(segments)

    def randomized_incremental_algorithm(self, segments):
        """
        Driver for the randomized incremental algorithm. Takes in a list of segments
        and calls add_new_segment() to process them

        :param segments: List of segments to add to the DAG
        """
        # random.Random(51).shuffle(segments)  # randomize step can be skipped

        for _ in range(0, len(segments)):
            segment = segments.pop(0)
            self.add_new_segment(segment)

    def add_new_segment(self, segment):
        """
        This function handles the logic for adding each endpoint and segment to the DAG
        There are three possible cases to consider
        1. The line segment partially intersects a trapezoid
        2. The line segment is completely inside an existing trapezoid
        3. The line segment completely cuts a trapezoid in half
        There are special functions to handle each situation, and their special cases
        :param segment: A line segment to add to the existing DAG
        """

        # Traverse the existing DAG and find the trapezoids the new segment intersects
        affected_trapezoids = list(self.find_trapezoids(self.head, segment))

        # If the segment only affects one trapezoid, we only have to consider case 2
        if len(affected_trapezoids) == 1:
            handle_case_2(segment, affected_trapezoids[0])

            # For visualizing the DAG after each step
            # visualizations.plot_dag(self, self.bbox, False)
            return

        # Find the trapezoids that contain the right and left endpoints, and remove
        # them from the affected trapezoid list
        left_point_trap = self.point_region_query(self.head, segment.p1)
        right_point_trap = self.point_region_query(self.head, segment.p2)
        affected_trapezoids.remove(left_point_trap)
        affected_trapezoids.remove(right_point_trap)

        # Check if the left and right endpoints already exist in the DAG
        # If so, we know we're handling a degenerate case
        degenerate_check_left = self.find_point(self.head, segment.p1)
        degenerate_check_right = self.find_point(self.head, segment.p2)

        # Adds the left endpoint to the DAG. We can trim the trapezoid to the left of the
        # point, but for the trapezoids above and below we might not know what to set as the
        # right bounding vertex so we save them for later
        up_and_down_traps = handle_case_1_left(segment.p1, segment, left_point_trap, degenerate_check_left)

        # Sort the affected trapezoids so they're processed left to right
        affected_trapezoids.sort(key=lambda x: x.data.trap.left_vert.x)

        # This handles trapezoids fully cut in half. We pass in information about the previous
        # trapezoids that were above/below as they might need to be merged or have their right
        # bounding vertex set
        for trapezoid in affected_trapezoids:
            up_and_down_traps = handle_case_3(segment, trapezoid, up_and_down_traps)

        # Handle adding the right endpoint to the DAG
        handle_case1_right(segment.p2, segment, right_point_trap, up_and_down_traps, degenerate_check_right)

        # For visualizing the DAG after each step
        # visualizations.plot_dag(self, self.bbox, False)

    def find_point(self, node, point):
        """
        Recursive function to find a point node in the DAG that's equivalent to a
        given point. Used to find degenerate points
        :param node: The current node we're traversing down
        :param point: An existing point
        :return: A point that matches the input point, if one exists. None otherwise
        """
        curr_node = node.data

        if isinstance(curr_node, LeafNode):
            return None

        if isinstance(curr_node, PointNode) and curr_node.point == point:
            return node

        left_point = self.find_point(curr_node.left, point)

        if left_point is not None:
            return left_point

        return self.find_point(curr_node.right, point)

    def point_region_query(self, node, point, print_path=False):
        """
        This function performs planar point location queries.
        Recursively travels through the DAG to find what trapezoid a point is in
        Prints along the way
        :param node: The current node being traversed
        :param point: The point being queried
        :param print_path: Whether to print a path or not
        :return: The trapezoid that the point is in
        """
        curr_node = node.data

        if print_path:
            print(curr_node, end=" ")

        if isinstance(curr_node, LeafNode):
            return node

        if isinstance(curr_node, PointNode):
            if not point.is_right_of(curr_node.point):
                return self.point_region_query(curr_node.left, point, print_path)
            else:
                return self.point_region_query(curr_node.right, point, print_path)

        if isinstance(curr_node, SegmentNode):
            if point.is_above(curr_node.segment):
                return self.point_region_query(curr_node.left, point, print_path)
            else:
                return self.point_region_query(curr_node.right, point, print_path)

    def find_trapezoids(self, node, segment):
        """
        Finds all the trapezoids that would be affected by adding a segment to the DAG
        :param node: The current node being traversed
        :param segment: The segment being added
        :return: An array containing every trapezoid that the segment touches
        """
        curr_node = node.data

        # If we've reached a leaf node, return a set containing the trapezoid found
        if isinstance(curr_node, LeafNode):
            return {node}

        # If we're at a point node, the segment can either lie
        # Fully to the left: find all trapezoids to the left of the point
        # Fully to the right: find all trapezoids to the right
        # Or the point lies within the segment's x bounds: union the left and right results
        if isinstance(curr_node, PointNode):
            if not segment.p2.is_right_of(curr_node.point):
                return self.find_trapezoids(curr_node.left, segment)
            elif segment.p1.is_right_of(curr_node.point):
                return self.find_trapezoids(curr_node.right, segment)
            else:
                return self.find_trapezoids(curr_node.left, segment).union(self.find_trapezoids(curr_node.right, segment))

        # As segments don't intersect, there's no way for a segment to be in a trapezoid
        # that's above another segment, AND a trapezoid that's below a segment at the same time
        # Thus, we only have to go left OR go right

        # The only exception is the right endpoint degenerate case, due to our
        # implementation making certain assumptions about where a trapezoids starts
        # (i.e. we're inclusive of the left bound of a trapezoid but not the right)
        if isinstance(curr_node, SegmentNode):
            seg_above = segment.is_above(curr_node.segment)

            # Special degenerate case
            if segment.p2 == curr_node.segment.p2 and seg_above:
                return self.find_trapezoids(curr_node.left, segment).union(self.find_trapezoids(curr_node.right, segment))

            # General case
            if seg_above:
                return self.find_trapezoids(curr_node.left, segment)
            else:
                return self.find_trapezoids(curr_node.right, segment)

    def create_output_matrix(self):
        """
        Creates an adjacency matrix which represents the DAG, where a 1 represents a connection
        The matrix also contains the sums of the rows and columns
        """
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
            # print(matrix[i])
        return matrix

    def traverse_all_nodes(self, node, connections_map, names):
        """
        Recursively traverses every node in the DAG to create a list of node names and
        a map of parents to children.
        Initially node is the head, and connections_map and names are empty
        :param node: Current node
        :param connections_map: Map from node name to its children
        :param names: List of node names, can include duplicates
        """
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
        if isinstance(curr_node, SegmentNode):
            seg_name = curr_node.segment.name
            names.append(seg_name)
            l_name = self.traverse_all_nodes(curr_node.left, connections_map, names)
            r_name = self.traverse_all_nodes(curr_node.right, connections_map, names)
            if seg_name in connections_map:
                connections_map.get(seg_name).append(l_name)
                connections_map.get(seg_name).append(r_name)
            else:
                connections_map[seg_name] = [l_name, r_name]
            return seg_name
        if isinstance(curr_node, LeafNode):
            trap_name = curr_node.trap.name
            names.append(trap_name)
            return trap_name

    def get_all_trapezoids(self, node):
        """
        Returns every leaf node in the DAG
        :param node: The node we're currently in
        :return: Array of all trapezoids in the DAG
        """
        curr_node = node.data

        if isinstance(curr_node, LeafNode):
            return {curr_node.trap}

        return self.get_all_trapezoids(curr_node.left).union(self.get_all_trapezoids(curr_node.right))

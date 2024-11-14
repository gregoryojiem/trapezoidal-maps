from data_structures.dag_structures import Node, PointNode, SegmentNode, LeafNode
from data_structures.geometric_structures import Trapezoid


def handle_case_2(segment, leaf_node):
    """
    This handles the case where a segment being added to the DAG is fully
    contained within a trapezoid
    :param segment: The segment being added
    :param leaf_node: A leaf node containing the trapezoid the segment is in
    """
    # Extract the trapezoid from the node
    trap = leaf_node.data.trap

    # Create four trapezoids using information from the existing trapezoid and segment
    left = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, trap.left_vert, segment.p1)))
    up = Node(LeafNode(Trapezoid(trap.top_seg, segment, segment.p1, segment.p2)))
    down = Node(LeafNode(Trapezoid(segment, trap.bot_seg, segment.p1, segment.p2)))
    right = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, segment.p2, trap.right_vert)))

    # Set up the correct node structure and change the DAG
    segment_node = Node(SegmentNode(up, down, segment))
    right_endpoint = Node(PointNode(segment_node, right, segment.p2))
    left_endpoint = PointNode(left, right_endpoint, segment.p1)

    # Replace the leaf node with the new sub-graph
    leaf_node.data = left_endpoint

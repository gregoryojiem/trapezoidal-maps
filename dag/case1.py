from data_structures.dag_structures import Node, PointNode, SegmentNode, LeafNode
from data_structures.geometric_structures import Trapezoid


def handle_case_1_left(left_endpoint, segment, leaf_node, degenerate_point):
    """
    This case handles adding the left endpoint of a segment to the DAG
    There is special handling for the degenerate case
    :param left_endpoint: The endpoint to add to the DAG
    :param segment: The segment we're adding to the DAG
    :param leaf_node: The trapezoid the left endpoint is in
    :param degenerate_point: A degenerate point, if one exists
    :return: The trapezoids that were created above and below the segment
    """
    # In the event we have a degenerate case, we don't need to do anything if the
    # new segment is BELOW the existing segment. It is handled by the other endpoint
    if degenerate_point is not None and degenerate_point.data.point.segment.p2.is_above(segment.p2):
        return

    # Extract the trapezoid from the node
    trap = leaf_node.data.trap

    # Handle creating the trapezoids above and below the segment being added
    # Initially, we assume that the trapezoid's right bound is the same as the segment's
    # right endpoint (we set the right bound properly in case 3 and case 1 right)
    up = Node(LeafNode(Trapezoid(trap.top_seg, segment, left_endpoint, segment.p2)))
    down = Node(LeafNode(Trapezoid(segment, trap.bot_seg, left_endpoint, segment.p2)))

    # Either the trapezoid above this segment, or the one below, will be bounded by
    # the right bounding vertex of the trapezoid we're in
    if not left_endpoint.is_above(trap.right_vert) or left_endpoint == trap.right_vert:
        up.data.trap.right_vert = trap.right_vert
    else:
        down.data.trap.right_vert = trap.right_vert

    # The left node is just the trapezoid we're in, but we trim the right wall
    # If we have a degenerate point, then we don't need to do any trimming
    if degenerate_point is not None:
        left_node = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, trap.left_vert, left_endpoint)))
        left_node.data.trap.name = trap.name
    else:
        existing_left_trapezoid = degenerate_point.data.left.data.trap
        left_node = Node(LeafNode(existing_left_trapezoid))
        # We also have to adjust the bottom segment of the trapezoid below this one
        down.data.trap.bot_seg = degenerate_point.data.point.segment

    # Set up the correct node structure and change the DAG
    segment_node = Node(SegmentNode(up, down, segment))
    point_node = PointNode(left_node, segment_node, left_endpoint)
    leaf_node.data = point_node

    # Return the above/below trapezoids for future cases to consider
    return [up, down]


def handle_case1_right(right_endpoint, segment, leaf_node, past_traps, degenerate_point):
    """
    This case handles adding the right endpoint of a segment to the DAG
    There is special handling for the degenerate case
    :param right_endpoint: The endpoint to add to the DAG
    :param segment: The segment we're adding to the DAG
    :param leaf_node: The trapezoid the right endpoint is in
    :param past_traps: Previous trapezoids above/below that we might have to merge
    :param degenerate_point: A degenerate point, if one exists
    """
    # In the event we have a degenerate case, we don't need to do anything if the
    # new segment is ABOVE the existing segment. It is handled by the other endpoint
    if degenerate_point is not None and not degenerate_point.data.point.segment.p1.is_above(segment.p1):
        return

    # Extract the trapezoid from the node
    trap = leaf_node.data.trap

    # Merge this trapezoid with the past trapezoid if it's continuing along the same top segment
    # then, extend right vertex of merged trapezoid
    # Otherwise, construct/trim the above and below trapezoids from the data we have
    merge_top_trap = past_traps is not None and past_traps[0].data.trap.top_seg == trap.top_seg
    merge_bottom_trap = past_traps is not None and past_traps[1].data.trap.bot_seg == trap.bot_seg

    if merge_top_trap:
        up = past_traps[0]
        past_traps[0].data.trap.right_vert = right_endpoint
    else:
        up_trap_left_bound = segment.p1 if segment.p1.is_right_of(trap.left_vert) else trap.left_vert
        up = Node(LeafNode(Trapezoid(trap.top_seg, segment, up_trap_left_bound, right_endpoint)))

    if merge_bottom_trap:
        down = past_traps[1]
        past_traps[1].data.trap.right_vert = right_endpoint
    else:
        down_trap_left_bound = segment.p1 if segment.p1.is_right_of(trap.left_vert) else trap.left_vert
        down = Node(LeafNode(Trapezoid(segment, trap.bot_seg, down_trap_left_bound, right_endpoint)))

    # if there's a degenerate point, we don't need to trim the right trapezoid, we just assign it to this node
    if degenerate_point is not None:
        right_node = Node(LeafNode(degenerate_point.data.right.data.trap))
    else:
        right_node = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, right_endpoint, trap.right_vert)))

    # Set up the correct node structure and change the DAG
    segment = Node(SegmentNode(up, down, segment))
    new_point = PointNode(segment, right_node, right_endpoint)

    # Return the above/below trapezoids for future cases to consider
    leaf_node.data = new_point


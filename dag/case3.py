from data_structures.dag_structures import Node, SegmentNode, LeafNode
from data_structures.geometric_structures import Trapezoid


def handle_case_3(segment, leaf_node, past_traps):
    """
    This handles the case where a segment being added to the DAG completely cuts
    a trapezoid in half

    For this function, we have to consider the trapezoids that were generated from
    previous case 1/case 3. We might need to merge them with the current region
    that's being cut in half, or set their right bound

    :param segment: The segment being added
    :param leaf_node: A leaf node containing the trapezoid being cut in half
    :param past_traps: The previous trapezoids above and below the last case handled
    :return: The trapezoids that were created above and below the segment
    """
    # Extract the trapezoid from the node
    trap = leaf_node.data.trap

    # If the above/below trapezoids from past cases continue along the same segment, then
    # they can be merged with the above/below trapezoids for this case.
    merge_top_trap = past_traps is not None and past_traps[0].data.trap.top_seg == trap.top_seg
    merge_bottom_trap = past_traps is not None and past_traps[1].data.trap.bot_seg == trap.bot_seg

    if merge_top_trap:
        up = past_traps[0]
    else:
        up = Node(LeafNode(Trapezoid(trap.top_seg, segment, trap.left_vert, trap.right_vert)))

    if merge_bottom_trap:
        down = past_traps[1]
    else:
        down = Node(LeafNode(Trapezoid(segment, trap.bot_seg, trap.left_vert, trap.right_vert)))

    # All trapezoids have some right bounding vertex
    # When making above/below trapezoids for left endpoints, we assume that the right bound
    # is the same as the right endpoint.
    # This is because there's no way to tell at that point
    # Here is where we actually set the correct right bounding vertices
    trim_top_trap = trap.right_vert.is_above(segment)

    if merge_top_trap and trim_top_trap:
        up.data.trap.right_vert = trap.right_vert
    elif merge_bottom_trap and not trim_top_trap:
        down.data.trap.right_vert = trap.right_vert

    # The DAG structure for case 3 is simple - a segment node with trapezoids above/below
    segment_node = SegmentNode(up, down, segment)
    leaf_node.data = segment_node

    # Return the above/below trapezoids for future cases to consider
    return [up, down]

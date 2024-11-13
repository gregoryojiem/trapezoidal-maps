from data_structures.dag_structures import Node, SegNode, Leaf
from data_structures.geometric_structures import Trapezoid


def handle_case3(seg, node_leaf, past_traps):
    """
    Replaces the Leaf node with a new tree that represents
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf node which contains the trapezoid
    :param past_traps: Trapezoids created that might be merged with this case
    :returns: Top and bottom nodes
    """
    trap = node_leaf.data.trap
    side_to_trim = node_leaf.data.trap.right_vert.is_above(seg)
    right_bound = node_leaf.data.trap.right_vert

    if past_traps is not None and past_traps[0].data.trap.top_seg == trap.top_seg:
        up = past_traps[0]
        if side_to_trim:
            up.data.trap.right_vert = right_bound
    else:
        up = Node(Leaf(Trapezoid(trap.top_seg, seg, trap.left_vert, trap.right_vert)))

    if past_traps is not None and past_traps[1].data.trap.bot_seg == trap.bot_seg:
        down = past_traps[1]
        if not side_to_trim:
            down.data.trap.right_vert = right_bound
    else:
        down = Node(Leaf(Trapezoid(seg, trap.bot_seg, trap.left_vert, trap.right_vert)))

    s = SegNode(up, down, seg)
    node_leaf.data = s
    return [up, down]

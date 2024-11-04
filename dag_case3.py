from dag_structures import Node, PointNode, SegNode, Leaf
from trapezoidal_map import Trapezoid


def handle_case3(seg, node_leaf, past_traps):
    """
    Replaces the Leaf node with a new tree that represents
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf node which contains the trapezoid
    :param past_traps: Trapezoids created that might be merged with this case
    :returns: Top and bottom nodes
    """
    trap = node_leaf.data.trap
    if past_traps[0].data.trap.top_seg == trap.top_seg:
        up = past_traps[0]
    else:
        up_right = seg.p2 if not seg.p2.is_right_of(trap.top_seg.p2) else trap.top_seg.p2
        up_left = seg.p1 if seg.p1.is_right_of(trap.top_seg.p1) else trap.top_seg.p1
        up = Node(Leaf(Trapezoid(trap.top_seg, seg, up_left, up_right)))

    if past_traps is not None and past_traps[0].data.trap.bot_seg == trap.bot_seg:
        down = past_traps[1]
    else:
        down_right = seg.p2 if not seg.p2.is_right_of(trap.bot_seg.p2) else trap.bot_seg.p2
        down_left = seg.p1 if seg.p1.is_right_of(trap.bot_seg.p1) else trap.bot_seg.p1
        down = Node(Leaf(Trapezoid(seg, trap.bot_seg, down_left, down_right)))

    s = SegNode(up, down, seg)
    node_leaf.data = s
    return [up, down]

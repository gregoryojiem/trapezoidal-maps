from dir_acyc_graph import Node, Internal, Leaf
from trapezoidal_map import Trapezoid


def handle_case3(seg, node_leaf):
    """
    Replaces the Leaf node with a new tree that represents
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf node which contains the trapezoid
    """
    trap = node_leaf.data.trap
    up_right = seg.p2 if not seg.p2.is_right_of(trap.top_seg.p2) else trap.top_seg.p2
    up_left = seg.p1 if seg.p1.is_right_of(trap.top_seg) else trap.top_seg.p1
    down_right = seg.p2 if not seg.p2.is_right_of(trap.bot_seg.p2) else trap.bot_seg.p2
    down_left = seg.p1 if seg.p1.is_right_of(trap.bot_seg) else trap.bot_seg.p1

    up = Node(Trapezoid(trap.top_seg, seg, up_left, up_right))
    down = Node(Trapezoid(seg, trap.bot_seg, down_left, down_right))
    s = Node(Internal(up, down))
    node_leaf.data = s

from dag_structures import Node, PointNode, SegNode, Leaf
from trapezoidal_map import Trapezoid


def handle_case1(point, seg, node_leaf):
    """
    Replaces the Leaf node with a new tree that represents
    Accounts for if p is a left or right end point
    :param point: Point in the trapezoid
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf containing the trapezoid
    """
    trap = node_leaf.data.trap
    is_left_end_point = seg.p1 == point
    if is_left_end_point:
        up_left = point
        up_right = seg.p2 if not seg.p2.is_right_of(trap.top_seg.p2) else trap.top_seg.p2
        down_left = point
        down_right = seg.p2 if not seg.p2.is_right_of(trap.bot_seg.p2) else trap.bot_seg.p2
    else:
        up_left = seg.p1 if seg.p1.is_right_of(trap.top_seg) else trap.top_seg.p1
        up_right = point
        down_left = seg.p1 if seg.p1.is_right_of(trap.bot_seg) else trap.bot_seg.p1
        down_right = point
    up = Node(Leaf(Trapezoid(trap.top_seg, seg, up_left, up_right)))
    down = Node(Leaf(Trapezoid(seg, trap.bot_seg, down_left, down_right)))
    s = Node(SegNode(up, down, seg))

    if is_left_end_point:
        lr_left = trap.top_seg.p1 if trap.top_seg.p1.is_right_of(trap.bot_seg.p1) else trap.bot_seg.p1
        lr_right = point
    else:
        lr_left = point
        lr_right = trap.top_seg.p2 if not trap.top_seg.p2.x <= trap.bot_seg.p2.x else trap.bot_seg.p2

    left_or_right = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, lr_left, lr_right)))

    if is_left_end_point:
        pl = left_or_right
        pr = s
    else:
        pl = s
        pr = left_or_right

    p = PointNode(pl, pr, point)
    node_leaf.data = p

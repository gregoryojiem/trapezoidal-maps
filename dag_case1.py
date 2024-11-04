from dag_structures import Node, PointNode, SegNode, Leaf
from trapezoidal_map import Trapezoid


def handle_case1_left(point, seg, node_leaf, degenerate_point):
    """
    TODO
    :param point: Point in the trapezoid
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf containing the trapezoid
    :returns: todo
    """
    trap = node_leaf.data.trap
    up_left = point
    up_right = seg.p2 if not seg.p2.is_right_of(trap.right_vert) else trap.right_vert
    up = Node(Leaf(Trapezoid(trap.top_seg, seg, up_left, up_right)))

    down_left = point
    down_right = seg.p2 if not seg.p2.is_right_of(trap.bot_seg.p2) else trap.bot_seg.p2
    down = Node(Leaf(Trapezoid(seg, trap.bot_seg, down_left, down_right)))

    s = Node(SegNode(up, down, seg))

    lr_left = trap.top_seg.p1 if trap.top_seg.p1.is_right_of(trap.bot_seg.p1) else trap.bot_seg.p1
    lr_right = point

    if degenerate_point is not None:
        left_node = degenerate_point.data.left
    else:
        left_node = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, lr_left, lr_right)))

    p = PointNode(left_node, s, point)
    node_leaf.data = p
    return [up, down]


def handle_case1_right(point, seg, node_leaf, past_traps, degenerate_point):
    """
    TODO
    :param point: Point in the trapezoid
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf containing the trapezoid
    :param past_traps: Trapezoids created that might be merged with this case
    """
    trap = node_leaf.data.trap

    if past_traps[0].data.trap.top_seg == trap.top_seg:
        up = past_traps[0]
    else:
        up_left = seg.p1 if seg.p1.is_right_of(trap.left_vert) else trap.left_vert
        up_right = point
        up = Node(Leaf(Trapezoid(trap.top_seg, seg, up_left, up_right)))

    if past_traps[1].data.trap.bot_seg == trap.bot_seg:
        down = past_traps[1]
    else:
        down_left = seg.p1 if seg.p1.is_right_of(trap.bot_seg.p1) else trap.bot_seg.p1
        down_right = point
        down = Node(Leaf(Trapezoid(seg, trap.bot_seg, down_left, down_right)))

    if degenerate_point is not None:
        right_node = degenerate_point.data.right
    else:
        right_right = trap.top_seg.p2 if not trap.top_seg.p2.x <= trap.bot_seg.p2.x else trap.bot_seg.p2
        right_node = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, point, right_right)))

    s = Node(SegNode(up, down, seg))
    p = PointNode(s, right_node, point)
    node_leaf.data = p


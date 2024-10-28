from dir_acyc_graph import Node, Internal, Leaf
from trapezoidal_map import Trapezoid


def handle_case1(p, seg, leaf):
    trap = leaf.data.trap
    is_left_end_point = True if seg.p1 == p else False

    if is_left_end_point:
        up_left = p
        up_right = seg.p2 if seg.p2.x <= trap.top_seg.x else trap.top_seg.p2
        down_left = p
        down_right = seg.p2 if seg.p2.x <= trap.bot_seg.x else trap.top_seg.p2
    else:
        up_left = seg.p1 if seg.p1.x >= trap.top_seg.x else trap.top_seg.p1
        up_right = p
        down_left = seg.p1 if seg.p1.x >= trap.bot_seg.x else trap.bot_seg.p1
        down_right = p
    up = Node(Leaf(Trapezoid(trap.top_seg, seg, up_left, up_right)))
    down = Node(Leaf(Trapezoid(seg, trap.bot_seg, down_left, down_right)))
    s = Node(Internal(up, down))

    if is_left_end_point:
        lr_left = trap.top_seg.p1 if trap.top_seg.p1.x >= trap.bot_seg.p1.x else trap.bot_seg.p1
        lr_right = p
    else:
        lr_left = p
        lr_right = trap.top_seg.p2 if trap.top_seg.p2.x <= trap.bot_seg.p2.x else trap.bot_seg.p2

    left_or_right = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, lr_left, lr_right)))

    if is_left_end_point:
        pl = left_or_right
        pr = s
    else:
        pl = s
        pr = left_or_right

    p = Node(Internal(pl, pr))
    leaf.data = p

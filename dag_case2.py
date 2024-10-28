from dir_acyc_graph import Internal, Leaf
from trapezoidal_map import Trapezoid


def handle_case2(seg, parent, leaf):
    """
    Replaces the Leaf node with a new tree that represents
    the new trapezoids
    :param seg: Segment that was added to the graph
    :param parent: Internal node that points to the Leaf
    :param leaf: Leaf node which contains the trapezoid
    """
    # TODO handle the case of multiple internal nodes pointing the trapezoid/region
    trap = leaf.trap
    u = Leaf(Trapezoid(trap.top_seg, seg, seg.p1, seg.p2))
    d = Leaf(Trapezoid(seg, trap.bot_seg, seg.p1, seg.p2))
    r = Leaf(Trapezoid(trap.top_seg, trap.bot_seg, seg.p2, trap.right_vert))
    l = Leaf(Trapezoid(trap.top_seg, trap.bot_seg, trap.left_vert, seg.p1))

    s = Internal(u, d)
    q = Internal(s, r)
    p = Internal(l, q)

    if parent.is_left():
        parent.left = p
    else:
        parent.right = p

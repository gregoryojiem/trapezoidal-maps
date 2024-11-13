from dag_structures import Node, PointNode, SegNode, Leaf
from geometric_structures import Trapezoid


def handle_case2(seg, node_leaf):
    """
    Replaces the Leaf node with a new tree that represents
    the new trapezoids
    :param seg: Segment that was added to the graph
    :param node_leaf: Leaf node which contains the trapezoid
    """
    trap = node_leaf.data.trap
    up = Node(Leaf(Trapezoid(trap.top_seg, seg, seg.p1, seg.p2)))
    down = Node(Leaf(Trapezoid(seg, trap.bot_seg, seg.p1, seg.p2)))
    right = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, seg.p2, trap.right_vert)))
    left = Node(Leaf(Trapezoid(trap.top_seg, trap.bot_seg, trap.left_vert, seg.p1)))

    s = Node(SegNode(up, down, seg))
    q = Node(PointNode(s, right, seg.p2))
    p = PointNode(left, q, seg.p1)
    node_leaf.data = p

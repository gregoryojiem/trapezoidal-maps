from data_structures.dag_structures import Node, PointNode, SegmentNode, LeafNode
from data_structures.geometric_structures import Trapezoid


def handle_case1_left(left_endpoint, seg, node_leaf, degenerate_point):
    """
    TODO
    """
    if degenerate_point is not None and degenerate_point.data.point.segment.p2.is_above(seg.p2):
        return

    trap = node_leaf.data.trap

    up = Node(LeafNode(Trapezoid(trap.top_seg, seg, left_endpoint, seg.p2)))
    down = Node(LeafNode(Trapezoid(seg, trap.bot_seg, left_endpoint, seg.p2)))

    if not left_endpoint.is_above(trap.right_vert) or left_endpoint == trap.right_vert:
        up.data.trap.right_vert = trap.right_vert
    else:
        down.data.trap.right_vert = trap.right_vert

    s = Node(SegmentNode(up, down, seg))

    if degenerate_point is not None:
        left_node = Node(LeafNode(degenerate_point.data.left.data.trap))
        down.data.trap.bot_seg = degenerate_point.data.point.segment
    else:
        left_node = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, trap.left_vert, left_endpoint)))
        left_node.data.trap.name = trap.name

    p = PointNode(left_node, s, left_endpoint)
    node_leaf.data = p
    return [up, down]


def handle_case1_right(right_endpoint, seg, node_leaf, past_traps, degenerate_point):
    """
    TODO
    """
    if not node_leaf.data.trap.top_seg.p1.is_above(seg.p1):
        return

    trap = node_leaf.data.trap

    # merge this trapezoid with the past trapezoid if it's continuing along the same top segment
    # then, extend right vertex of merged trapezoid
    if past_traps[0].data.trap.top_seg == trap.top_seg:
        up = past_traps[0]
        past_traps[0].data.trap.right_vert = right_endpoint
    else:
        up_left = seg.p1 if seg.p1.is_right_of(trap.left_vert) else trap.left_vert
        up = Node(LeafNode(Trapezoid(trap.top_seg, seg, up_left, right_endpoint)))

    # merge bottom trapezoid and extend right vertex
    if past_traps[1].data.trap.bot_seg == trap.bot_seg:
        down = past_traps[1]
        past_traps[1].data.trap.right_vert = right_endpoint
    else:
        down_left = seg.p1 if seg.p1.is_right_of(trap.left_vert) else trap.left_vert
        down = Node(LeafNode(Trapezoid(seg, trap.bot_seg, down_left, right_endpoint)))

    # if there's a degenerate point, we don't need to trim the right trapezoid, we just assign it to this node
    if degenerate_point is not None:
        right_node = Node(LeafNode(degenerate_point.data.right.data.trap))
    else:
        right_node = Node(LeafNode(Trapezoid(trap.top_seg, trap.bot_seg, right_endpoint, trap.right_vert)))

    segment = Node(SegmentNode(up, down, seg))
    new_point = PointNode(segment, right_node, right_endpoint)
    node_leaf.data = new_point


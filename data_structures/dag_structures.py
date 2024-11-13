class Node:
    """
    A reference to a node, which may be a PointNode, a SegmentNode, or a LeafNode.
    The purpose of this class is to be a mutable reference; when modified, all
    instances of an object will reflect
    that change
    """

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)


class LocationNode:
    """
    An abstract class that represents a spatial node in a DAG, where left/right
    gives information about where children are located relative to the root
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right


class PointNode(LocationNode):
    """
    A DAG node that stores a point and two children, where left children are located
    to the left of the point, and right children to the right

    Synonymous with the x-node discussed in lecture
    """

    def __init__(self, left, right, point):
        super().__init__(left, right)
        self.point = point

    def __str__(self):
        return str(self.point)


class SegmentNode(LocationNode):
    """
    A DAG node that stores a segment and two children, where left children are located
    above the segment, and right children below

    Synonymous with the y-node discussed in lecture
    """

    def __init__(self, left, right, seg):
        super().__init__(left, right)
        self.seg = seg

    def __str__(self):
        return str(self.seg)


class LeafNode:
    """
    A DAG node that stores a trapezoid, which are always leaf nodes
    """

    def __init__(self, trap):
        self.trap = trap

    def __str__(self):
        return str(self.trap)

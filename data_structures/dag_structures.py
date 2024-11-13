class Node:
    """
    Stores other node types so parent nodes do not have to update who their children are,
    instead update the child by replacing its test_data
    """
    def __init__(self, data):
        """
        Creates a Node to store Nodes
        :param data: Node to store
        """
        self.data = data

    def __str__(self):
        return str(self.data)


class Internal:
    """
    Abstract class Internal Node for the DAG
    An Internal Node must have both a left and right child
    """
    def __init__(self, left, right):
        """
        Creates an Internal Node containing left and right children
        :param left: Left child Node
        :param right: Right child Node
        """
        self.left = left
        self.right = right

    def is_child_left(self, node):
        """
        Check if the node is the left child of this Node
        :param node: Node to check against
        :returns: True if the child is on the left, False if it is on the right, undefined if node is not a child
        """
        if self.left == node:
            return True
        elif self.right == node:
            return False


class PointNode(Internal):
    """
    Point Node for the DAG
    Contains left and right children and the Point
    """

    def __init__(self, left, right, point):
        """
        Creates a Point Node containing left and right children and the Point
        :param left: Left child Node
        :param right: Right child Node
        :param point: Current Point
        """
        super().__init__(left, right)
        self.point = point

    def __str__(self):
        return str(self.point)


class SegNode(Internal):
    """
    Segment Node for the DAG
    Contains left and right children and the Segment
    """
    def __init__(self, left, right, seg):
        """
        Creates a Segment Node containing left and right children and the Segment
        :param left: Left child Node
        :param right: Right child Node
        :param seg: Current Segment
        """
        super().__init__(left, right)
        self.seg = seg

    def __str__(self):
        return str(self.seg)


class Leaf:
    """
    Leaf Node for the DAG
    Contains a Trapezoid
    """
    def __init__(self, trap):
        """
        Creates a Leaf containing a Trapezoid
        :param trap: Trapezoid to store
        """
        self.trap = trap

    def __str__(self):
        return str(self.trap)
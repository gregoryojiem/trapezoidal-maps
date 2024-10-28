class Point:
    """
    Todo
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment:
    """
    Todo
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"{self.p1}-{self.p2}"


class Trapezoid:
    def __init__(self, top_seg, bot_seg, left_vert, right_vert):
        """
        Creates a trapezoid
        :param top_seg: Top line Segment
        :param bot_seg: Bottom line Segment
        :param left_vert: Left vertex
        :param right_vert: Right vertex
        """
        self.top_seg = top_seg
        self.bot_seg = bot_seg
        self.left_vert = left_vert
        self.right_vert = right_vert


class TrapezoidalMap:
    """
    Todo
    """
    def __init__(self, line_segments, bbox):
        self.trapezoids = []
        self.line_segments = line_segments
        self.bbox = bbox

    def __str__(self):
        return "[" + "\n".join("{!s}".format(x) for x in self.line_segments) + "]"

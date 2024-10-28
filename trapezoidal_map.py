class Point:
    """
    Todo
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_right_of(self, point):
        return self.x > point.x

    def is_above(self, obj): #todo refactor
        if isinstance(obj, Point):
            return self.y > obj.y

        seg = obj
        cross_product = (seg.p2.x - seg.p1.x) * (self.y - seg.p1.y) - (seg.p2.y - seg.p1.y) * (self.x - seg.p1.x)
        return cross_product > 0

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment:
    """
    Todo
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_lower_point(self):
        return min(self.p1, self.p2, key=lambda p: p.y)

    def get_higher_point(self):
        return max(self.p1, self.p2, key=lambda p: p.y)

    def __str__(self):
        return f"{self.p1}-{self.p2}"


class Trapezoid:
    """
    Trapezoid defined by a top and bottom segment and a left and right vertex
    """
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
    Holds information about the bounding box, the line segments, and the DAG
    """
    def __init__(self, line_segments, bbox):
        """
        Contains important information to the algorithm
        :param line_segments: List of line segments
        :param bbox: Trapezoid of the bounding box for the line segments
        """
        bbox_p1 = Point(bbox[0], bbox[1])
        bbox_p2 = Point(bbox[2], bbox[3])
        top_seg = Segment(Point(bbox_p1.x, bbox_p2.y), bbox_p2)
        bot_seg = Segment(bbox_p1, Point(bbox_p2.x, bbox_p1.y))
        self.bbox = Trapezoid(top_seg, bot_seg, bbox_p1, bbox_p2)
        self.line_segments = line_segments

    def __str__(self):
        return "[" + "\n".join("{!s}".format(x) for x in self.line_segments) + "]"

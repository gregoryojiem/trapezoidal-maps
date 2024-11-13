class Point:
    """
    Class for a 2D point
    Stores the x and y coordinate
    """
    def __init__(self, x, y, name):
        """
        Initialize a point with x and y coordinates
        :param x: x coordinate
        :param y: y coordinate
        """
        self.x = x
        self.y = y
        self.name = name
        self.segment = None

    def is_right_of(self, point):
        """
        Check if this point's x coordinate is greater than the x coordinate of another point
        :param point: Point to check against
        :returns: True if this point is to the right of the other point, False otherwise
        """
        return self.x > point.x

    def is_above(self, obj): #todo refactor
        """
        Checks if this Point is above the given Point or Segment
        By checking the y coordinate, or the cross product
        :param obj: A Point or a Segment
        :returns: For a Point, True, if this point is above the point, False otherwise
        For a Segment, True if this point  is above the segment, False otherwise
        """
        if isinstance(obj, Point):
            return self.y > obj.y

        seg = obj
        above_seg_p1 = self.is_above(seg.p1)
        above_seg_p2 = self.is_above(seg.p2)

        if above_seg_p1 and above_seg_p2:
            return True

        if not above_seg_p2 and not above_seg_p2:
            return False

        # TODO testing
        cross_product = (seg.p2.x - seg.p1.x) * (self.y - seg.p1.y) - (seg.p2.y - seg.p1.y) * (self.x - seg.p1.x)
        return cross_product > 0

    def set_segment(self, segment):
        self.segment = segment

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.name + f"({self.x}, {self.y})"


class Segment:
    """
    Todo
    """
    def __init__(self, p1, p2, name):
        self.p1 = p1
        self.p2 = p2
        self.name = name

    def get_y_at_x(self, x):
        """Returns the y-coordinate of the line segment at the given x-value."""
        slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)  # Calculate slope
        y = slope * (x - self.p1.x) + self.p1.y  # Calculate y-intercept
        return y

    def is_above(self, otherSeg):
        leftmost_x = max(self.p1.x, otherSeg.p1.x)
        rightmost_x = min(self.p2.x, otherSeg.p2.x)
        x = (leftmost_x + rightmost_x) / 2
        return self.get_y_at_x(x) > otherSeg.get_y_at_x(x)

    def __str__(self):
        return self.name + f" {self.p1}-{self.p2}"


class Trapezoid:
    """
    Trapezoid defined by a top and bottom segment and a left and right vertex
    """

    id_counter = 0

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
        self.name = f"T{self.id_counter}"
        Trapezoid.id_counter += 1

    def get_vertices(self):
        leftmost_x = self.left_vert.x
        rightmost_x = self.right_vert.x
        top_left_y = self.top_seg.get_y_at_x(leftmost_x)
        top_right_y = self.top_seg.get_y_at_x(rightmost_x)
        bot_left_y = self.bot_seg.get_y_at_x(leftmost_x)
        bot_right_y = self.bot_seg.get_y_at_x(rightmost_x)

        vertices = [
            (leftmost_x, bot_left_y),
            (rightmost_x, bot_right_y),
            (rightmost_x, top_right_y),
            (leftmost_x, top_left_y),
        ]

        if vertices[1] == vertices[2]:
            return [vertices[0], vertices[1], vertices[3]]

        if vertices[0] == vertices[3]:
            return [vertices[0], vertices[1], vertices[2]]

        return vertices

    def __str__(self):
        return self.name
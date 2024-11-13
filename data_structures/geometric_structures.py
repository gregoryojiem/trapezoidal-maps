class Point:
    """
    Represents a 2D point, with various functions for common operations
    """

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name  # Used to identify the point based on when it was read in, e.g. P1, P2, Q1, etc.
        self.segment = None

    def set_segment(self, segment):
        self.segment = segment

    def is_right_of(self, point):
        """
        Checks whether this point is to the right of another point
        :param point: point to compare
        :returns: True if this point is to the right of the other, False otherwise
        """
        return self.x > point.x

    def is_above(self, obj):
        """
        Checks whether this point is above a segment or another point
        For a point, only y values are compared
        For a segment, the line equation is used to determine above-ness
        :param obj: An instance of Point or Segment
        :returns: True if above, False otherwise
        """
        if isinstance(obj, Point):
            return self.y > obj.y

        if not isinstance(obj, Segment):
            raise TypeError("Can only compare points to points or segments")

        return self.y > obj.get_y_at_x(self.x)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.name + f"({self.x}, {self.y})"


class Segment:
    """
    Represents a line segment, with various functions for common operations
    p1 is guaranteed to be the leftmost point
    """

    def __init__(self, p1, p2, name):
        self.p1 = p1
        self.p2 = p2
        self.name = name  # Used to identify the segment based on when it was read in, e.g. S1, S2

    def get_slope(self):
        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    def get_y_at_x(self, x):
        """
        Returns the y-coordinate of the line segment at the given x-value
        :param x: The x value to use
        :returns: y-coordinate at x
        """
        return self.get_slope() * (x - self.p1.x) + self.p1.y  # point-slope form

    def is_above(self, otherSegment):
        """
        Used to check if one segment is above another by comparing an
        overlapping region. The segments must overlap to some degree
        :param otherSegment: Other segment to compare
        :returns: True if this point is above the other, False otherwise
        """
        leftmost_x = max(self.p1.x, otherSegment.p1.x)
        rightmost_x = min(self.p2.x, otherSegment.p2.x)
        x = (leftmost_x + rightmost_x) / 2
        return self.get_y_at_x(x) > otherSegment.get_y_at_x(x)

    def __str__(self):
        return self.name + f" {self.p1}-{self.p2}"


class Trapezoid:
    """
    Represents a trapezoid, defined by a top/bottom segment and left/right vertex
    """

    id_counter = 0  # Used to name trapezoids in the order they're created

    def __init__(self, top_seg, bot_seg, left_vert, right_vert):
        self.top_seg = top_seg
        self.bot_seg = bot_seg
        self.left_vert = left_vert
        self.right_vert = right_vert
        self.name = f"T{self.id_counter}"
        Trapezoid.id_counter += 1

    def get_vertices(self):
        """
        Returns an array of vertices that represent the trapezoid
        Used mainly for matplotlib visualization
        """
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

        # Handle degenerate case
        if vertices[1] == vertices[2]:
            return [vertices[0], vertices[1], vertices[3]]

        if vertices[0] == vertices[3]:
            return [vertices[0], vertices[1], vertices[2]]

        return vertices

    def __str__(self):
        return self.name

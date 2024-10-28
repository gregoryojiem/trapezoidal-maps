class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    """
    Bla bla
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Trapezoid:
    def __init__(self, top_seg, bot_seg, left_vert, right_vert):
        self.top_seg = top_seg
        self.bot_seg = bot_seg
        self.left_vert = left_vert
        self.right_vert = right_vert


class TrapezoidalMap:
    def __init__(self, line_segments):
        self.trapezoids = []
        self.line_segments = line_segments


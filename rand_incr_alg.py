from random import shuffle
from trapezoidal_map import Segment, Point, TrapezoidalMap


def randomized_incremental_algorithm(trap_map):
    shuffle(trap_map.line_segments)
    segments = trap_map.line_segments
    num_segments = len(segments)
    for _ in range(0, num_segments):
        segment = segments.pop(0)
        trap_map.dag.add_new_segment(segment)

from random import shuffle
from trapezoidal_map import Segment, Point, TrapezoidalMap


def randomized_incremental_algorithm(trap_map):
    shuffle(trap_map.line_segments)
    print(trap_map)

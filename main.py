"""
CS716 Assignment 3 - Trapezoidal Maps and Planar Point Location
Authors:
Gregory Ojiem, gro3228
Holden Lalumiere, hll7371
"""

import visualizations
from trapezoidal_map import Segment, Point, TrapezoidalMap
from rand_incr_alg import randomized_incremental_algorithm


def read_input(file_path):
    with open(file_path, 'r') as file:
        num_segments = int(file.readline())
        bbox = [int(x) for x in file.readline().split()]
        segments = []

        for _ in range(num_segments):
            line = [int(x) for x in file.readline().split()]
            p1 = Point(line[0], line[1])
            p2 = Point(line[2], line[3])
            segments.append(Segment(p1, p2))

        return segments, bbox


def main():
    line_segments, bbox = read_input("data/gro3228.txt")
    trapezoidal_map = TrapezoidalMap(line_segments, bbox)
    randomized_incremental_algorithm(trapezoidal_map)
    visualizations.plot_segments(line_segments, bbox)


if __name__ == '__main__':
    main()


"""
CS716 Assignment 3 - Trapezoidal Maps and Planar Point Location
Authors:
Gregory Ojiem, gro3228
Holden Lalumiere, hll7371
"""

import matplotlib.pyplot as plt
import visualizations
from trapezoidal_map import Segment, Point, TrapezoidalMap
from rand_incr_alg import randomized_incremental_algorithm


def read_input(file_path):
    """
    Reads input file from the file path
    First line is number of line segments
    Second line is the bounding box which contains all line segments
    in p1x, p1y, p2x, p2y format
    The rest of the lines are the n line segments
    :param file_path: File path to read input from
    """
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
    line_segments, bbox = read_input("data/hll7371.txt")
    trapezoidal_map = TrapezoidalMap(line_segments, bbox)
    dag = randomized_incremental_algorithm(trapezoidal_map, bbox)
    visualizations.regions_seen = []
    visualizations.trap_region_count = 0
    visualizations.plot_dag(dag, bbox)
    print("There were: " + str(visualizations.trap_region_count) + " trapezoids")

if __name__ == '__main__':
    main()

"""
CS716 Assignment 3 - Trapezoidal Maps and Planar Point Location
Authors:
Gregory Ojiem, gro3228
Holden Lalumiere, hll7371
"""

import visualizations
from random import shuffle


class Segment:
    """
    Bla bla
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def read_input(file_path):
    with open(file_path, 'r') as file:
        num_segments = int(file.readline())
        bbox = [int(x) for x in file.readline().split()]
        segments = []

        for _ in range(num_segments):
            line = [int(x) for x in file.readline().split()]
            segments.append(Segment((line[0], line[1]), (line[2], line[3])))

        return shuffle(segments), bbox


def main():
    line_segments, bbox = read_input("data/gro3228.txt")
    visualizations.plot_segments(line_segments, bbox)

if __name__ == '__main__':
    main()


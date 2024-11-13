"""
CS716 Assignment 3 - Trapezoidal Maps and Planar Point Location
Authors:
Gregory Ojiem, gro3228
Holden Lalumiere, hll7371
"""

import visualizations
from sys import argv
from geometric_structures import Segment, Point, Trapezoid
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

        for i in range(num_segments):
            line = [int(x) for x in file.readline().split()]
            x1, y1, x2, y2 = line
            if x1 > x2:
                x1, y1, x2, y2 = x2, y2, x1, y1

            p1 = Point(x1, y1, f"P{i + 1}")
            p2 = Point(x2, y2, f"Q{i + 1}")
            segment = Segment(p1, p2, f"S{i + 1}")
            segments.append(segment)
            p1.set_segment(segment)
            p2.set_segment(segment)

        bbox_p1 = Point(bbox[0], bbox[1], "B1")
        bbox_p2 = Point(bbox[2], bbox[3], "B2")
        top_seg = Segment(Point(bbox_p1.x, bbox_p2.y, "B3"), bbox_p2, "STop")
        bot_seg = Segment(bbox_p1, Point(bbox_p2.x, bbox_p1.y, "B4"), "SBot")
        bbox = Trapezoid(top_seg, bot_seg, bbox_p1, bbox_p2)

        return segments, bbox


def create_csv(matrix, filename):
    """
    Creates a csv file with the matrix given under "filenameOut.csv"
    :param matrix: Matrix to save
    :param filename: File name to save to
    """
    f = open(f"{filename}Out.csv", "w")
    for row in matrix:
        for j in range(len(row)):
            entry = row[j]
            if entry is None:
                entry = ""
            f.write(f"{entry},")
        f.write("\n")


def main():
    """
    Runs all parts of the program.
    Reads the input file, creates the initial map, the DAG, creates the adjacency matrix,
    saves the matrix, visualizes the Trapezoids, and asks for input to test what Trapezoid a point is in.
    """
    filename = argv[1]
    line_segments, bbox = read_input(filename)
    dag = randomized_incremental_algorithm(line_segments, bbox)
    matrix = dag.create_output_matrix()
    create_csv(matrix, filename.split(".")[0])
    visualizations.regions_seen = []
    visualizations.trap_region_count = 0
    visualizations.plot_dag(dag, bbox)
    print("There were: " + str(visualizations.trap_region_count) + " trapezoids")

    input_info = input("Enter a point in the format 'x y'\n")
    point_info = list(map(int, input_info.split(" ")))
    dag.find_point_region(dag.head, Point(point_info[0], point_info[1], "N/A"), True)


if __name__ == '__main__':
    main()
